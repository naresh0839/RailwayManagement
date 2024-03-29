from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

import MySQLdb

def home(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/dashboard/")
	else:
		return HttpResponse(render(request, "home.html"))

def aboutus(request):
	return HttpResponse(render(request, "aboutus.html"))
	
@login_required
def dashboard(request):
	if request.method == "POST":
		fstation = request.POST.get('fstation')
		sstation = request.POST.get('sstation')
		doj = request.POST.get('date_of_journey')

		invalid = True

		if fstation == sstation:
			return HttpResponse("station code must be different")

		c = connection.cursor()
		c.execute('SELECT * FROM Station WHERE Station_Code = "%s" ' %(fstation))

		if len(c.fetchall())==0:
			invalid = False

		c.execute('SELECT * FROM Station WHERE Station_Code = "%s" ' %(sstation))

		if len(c.fetchall())==0:
			invalid = False

		if not invalid:
			context = {"show":False, "invalid":True,"notfound":False}
			return HttpResponse(render(request, "dashboard.html", context))

		c.execute('''SELECT a.Train_No FROM Stoppage as a join Stoppage as b on a.Train_No = b.Train_No 
			         WHERE a.Station_Code = "%s" and b.Station_Code = "%s" ''' %(fstation, sstation))
		
		trains = c.fetchall()
		if len(trains) == 0:
			context = {"show":False, "invalid":False, "notfound":True}
			return HttpResponse(render(request, "dashboard.html", context))	
		
		# finding valid trains out of the initial list i.e. final_station's arrival time must be more than initial_station's arrival time
		valid_trains = []
		for x in trains:
			c.execute('''SELECT Arrival_Time FROM Stoppage WHERE Train_No = "%s" and Station_Code = "%s" ''' %(x[0], fstation))
			a = c.fetchone()
			c.execute('''SELECT Arrival_Time FROM Stoppage WHERE Train_No = "%s" and Station_Code = "%s" ''' %(x[0], sstation))
			b = c.fetchone()
			if b is None or a is None:
				continue
			if b[0] > a[0]:
				valid_trains.append(x[0])
		
		# for finding the number of seats available at the given specified date of travel
		train_seats = []
		for x in valid_trains:
			c.execute(''' SELECT * FROM Seats WHERE Train_No = "%s" and Date = "%s" ''' %(x, doj))
			a = c.fetchone()
			seat_list_train = []
			seat_list_train.append(x)
			if a is None:
				seat_list_train.append(0)
				seat_list_train.append(0)
				seat_list_train.append(0)
				seat_list_train.append(0)
			else:
				seat_list_train.append(a[2])
				seat_list_train.append(a[3])
				seat_list_train.append(a[4])
				seat_list_train.append(a[5])
			train_seats.append(seat_list_train)
		context = {"trains":train_seats, "show":True, "date_of_journey":doj}
		return HttpResponse(render(request, "available_trains.html", context))		
	return HttpResponse(render(request, "dashboard.html", {"show":False,"invalid":False,"notfound":False}))

@login_required
def download_ticket(request):
	if request.method == "POST":
		ticketno = int(request.POST.get('ticketno'))
		c = connection.cursor()
		c.execute('SELECT Username FROM Ticket WHERE Ticket_No = %d' %(ticketno))
		user = c.fetchone()
		if user == None:
			context = {"owner": True, "show":False}
			return HttpResponse(render(request, "download_ticket.html", context))
		if user[0] == request.user.username:

			c.execute('SELECT * FROM Ticket WHERE Ticket_No = %d' %(ticketno))
			tickets = c.fetchone()
			c.execute('SELECT * FROM Passenger WHERE Ticket_No = %d' %(ticketno))
			passenger = c.fetchone()
			context = {"ticket":tickets, "passenger":passenger, "show":True, "owner":False}
			if tickets == None:
				return HttpResponse("Invalid Ticket No!!")
			else:
				return HttpResponse(render(request, "download_ticket.html", context))
		else :
			context = {"owner": True, "show":False}
			return HttpResponse(render(request, "download_ticket.html", context))
	else:
		return HttpResponse(render(request, "download_ticket.html", {"show":False,"owner":False}))

@login_required
def traininfo(request):
	if request.method == "POST":
		trainno = request.POST.get('trainno')
		if trainno == "" or 'e' in trainno:
			return HttpResponse("invalid train number")		
		trainno = int(trainno)
		c = connection.cursor()
		c.execute('SELECT * FROM Train WHERE Train_No = %d' %(trainno))
		train = c.fetchone()
		c.execute('SELECT * FROM Stoppage WHERE Train_No = %d' %(trainno))
		stoppage = c.fetchall()

		c.execute('SELECT * FROM Station')
		scode = {}
		for row in c.fetchall():
			scode[str(row[0])] = str(row[1])
		station = {}
		for row in stoppage:
			station[str(row[1])] = scode[str(row[1])]

		context = {"info":train, "stop":stoppage, "station":station, "show":True,"invalid":False}
		if train == None:
			context = {"show":False, "invalid":True}
			return HttpResponse(render(request, "traininfo.html", context))
		else:
			return HttpResponse(render(request, "traininfo.html", context))
	else:
		return HttpResponse(render(request, "traininfo.html", {"show":False,"invalid":False}))

@login_required
def findtrains(request):
	if request.method == "POST":
		fstation = request.POST.get('fstation')
		sstation = request.POST.get('sstation')
		doj = request.POST.get('date_of_journey')

		invalid = True

		if len(fstation) == 0 or len(sstation) == 0:
			return HttpResponse("station code can't be empty")
		
		for c in fstation:
			if c == " ":
				return HttpResponse("space is not allowed")

		for c in sstation:
			if c == " ":
				return HttpResponse("space is not allowed")

		if fstation == sstation:
			return HttpResponse("station code must be different")

		c = connection.cursor()
		c.execute('SELECT * FROM Station WHERE Station_Code = "%s" ' %(fstation))

		if len(c.fetchall())==0:
			invalid = False

		c.execute('SELECT * FROM Station WHERE Station_Code = "%s" ' %(sstation))

		if len(c.fetchall())==0:
			invalid = False

		if not invalid:
			context = {"show":False, "invalid":True,"notfound":False}
			return HttpResponse(render(request, "findtrains.html", context))

		c.execute('''SELECT a.Train_No FROM Stoppage as a join Stoppage as b on a.Train_No = b.Train_No 
			         WHERE a.Station_Code = "%s" and b.Station_Code = "%s" ''' %(fstation, sstation))
		
		trains = c.fetchall()
		if len(trains) == 0:
			context = {"show":False, "invalid":False, "notfound":True}
			return HttpResponse(render(request, "findtrains.html", context))	
		
		# finding valid trains out of the initial list i.e. final_station's arrival time must be more than initial_station's arrival time
		valid_trains = []
		for x in trains:
			c.execute('''SELECT Arrival_Time FROM Stoppage WHERE Train_No = "%s" and Station_Code = "%s" ''' %(x[0], fstation))
			a = c.fetchone()
			c.execute('''SELECT Arrival_Time FROM Stoppage WHERE Train_No = "%s" and Station_Code = "%s" ''' %(x[0], sstation))
			b = c.fetchone()
			if b is None or a is None:
				continue
			if b[0] > a[0]:
				valid_trains.append(x[0])
		
		# for finding the number of seats available at the given specified date of travel
		train_seats = []
		for x in valid_trains:
			c.execute(''' SELECT * FROM Seats WHERE Train_No = "%s" and Date = "%s" ''' %(x, doj))
			a = c.fetchone()
			seat_list_train = []
			seat_list_train.append(x)
			if a is None:
				seat_list_train.append(0)
				seat_list_train.append(0)
				seat_list_train.append(0)
				seat_list_train.append(0)
			else:
				seat_list_train.append(a[2])
				seat_list_train.append(a[3])
				seat_list_train.append(a[4])
				seat_list_train.append(a[5])
			train_seats.append(seat_list_train)
	
		context = {"trains":train_seats, "show":True}
		return HttpResponse(render(request, "available_trains.html", context))		
	else:
		return HttpResponse(render(request, "findtrains.html", {"show":False,"invalid":False,"notfound":False}))	

@login_required
def ticket(request, train_no=None, doj=None):
	if train_no==None:
		return HttpResponseRedirect("/dashboard/")
	if doj==None:
		return HttpResponseRedirect("/dashboard")
	if request.method == "POST":
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		username = request.user.username
		gender = request.POST.get('gender')
		age = request.POST.get('age')
		tclass = request.POST.get('tclass')
		number = request.POST.get('number')

		c = connection.cursor()

		c.execute("SELECT * FROM Train where Train_No = '%s' " %(train_no))

		train = c.fetchall()

		if len(train) == 0:
			return HttpResponse("Incorrect Train Number")

		train = train[0]

		alpha = []
		ch = 'a'
		for i in range(0, 26):
			alpha.append(ch)
			ch = chr(ord(ch) + 1)
			
		invalid = False
		
		if len(fname) == 0:
			invalid = True

		for c in fname:
			if c not in alpha:
				invalid = True
				break	

		if invalid:
			return HttpResponse("invalid fname, characters allowed [a-z]")

		invalid = False
		
		if len(lname) == 0:
			invalid = True

		for c in lname:
			if c not in alpha:
				invalid = True
				break

		if invalid:
			return HttpResponse("invalid lname, characters allowed [a-z]")

		if age == "" or 'e' in age or int(age) > 100:
			return HttpResponse("invalid age")

		num = []
		zer = '0'
		for i in range(0, 10):
			num.append(zer)
			zer = chr(ord(zer) + 1)
		
		invalid = False

		if len(number) != 10:
			invalid = True
		for c in number:
			if c not in num:
				invalid = True
				break

		if invalid:
			return HttpResponse("invalid phone number")

		gender = gender[0]
		if str(tclass) == "sleeper" and int(train[2]) <= 0:
			return HttpResponse("seat not available in sleeper class")
		if str(tclass) == "first class ac" and int(train[3]) <= 0:
			return HttpResponse("seat not available in first class ac")
		if str(tclass) == "second class ac" and int(train[4]) <= 0:
			return HttpResponse("seat not available in second class ac")
		if str(tclass) == "third class ac" and int(train[5]) <= 0:
			return HttpResponse("seat not available in third class ac")

		c = connection.cursor()		
		c.execute("SELECT * FROM Ticket")
		maximum = 0
		for row in c.fetchall():
			maximum = max(maximum, int(row[0]))

		ticketno = (maximum + 1)
		print(ticketno)
		import datetime
		now = datetime.datetime.now()
		now = str(now)
		jdate = (now.split())[0]
		print(username)
		c.execute("SELECT * FROM account WHERE Username='%s'" %(username))

		user1=c.fetchall()
		
		c.execute('''INSERT INTO Ticket VALUES("%s", "%s", "%s", "%s")
					 ''' %(ticketno, train_no, jdate, username))

		c.execute('''INSERT INTO Passenger(First_name, Last_name, Gender, Phone_No,
			         Ticket_No, Age, Class) VALUES
			         ("%s", "%s", "%s", "%s", "%s", "%s", "%s")
			         ''' %(fname, lname, gender, number, ticketno, age, tclass))
        
		if str(tclass) == "sleeper":
			c.execute('''UPDATE Train set Seat_Sleeper = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[2])-1, train_no))
		if str(tclass) == "first class ac":
			c.execute('''UPDATE Train set Seat_First_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[3])-1, train_no))
		if str(tclass) == "second class ac":
			c.execute('''UPDATE Train set Seat_Second_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[4])-1, train_no))
		if str(tclass) == "third class ac":
			c.execute('''UPDATE Train set Seat_Third_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[5])-1, train_no))			

		context = {"ticket_no":ticketno, "show":True}
		return HttpResponse(render(request, "ticket.html", context))
	else:
		c = connection.cursor()
		c.execute(''' SELECT * FROM Seats WHERE Train_No = "%s" and Date = "%s" ''' %(train_no, doj))
		a = c.fetchone()
		seat_list = []
		seat_list.append(train_no)
		total_seats = 0
		if a is None:
			seat_list.append(0)
			seat_list.append(0)
			seat_list.append(0)
			seat_list.append(0)
			seat_list.append(0)
		else:
			seat_list.append(a[2])
			seat_list.append(a[3])
			seat_list.append(a[4])
			seat_list.append(a[5])
			seat_list.append(a[2] + a[3] + a[4] + a[5])
		if seat_list[5] == 0:
			return HttpResponse(render(request, "ticket.html", {"seat_list":seat_list, "show":False, "doj":doj, "no_seats":True}))
		else:
			return HttpResponse(render(request, "ticket.html", {"seat_list":seat_list, "show":False, "doj":doj, "no_seats":False}))

def signup(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/dashboard/")
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		phone_number = request.POST.get('phone_number')
		print(username)
		print(password)
		c = connection.cursor()
		c.execute('SELECT * FROM account WHERE username = "%s" ' %(username))
		users = c.fetchall()
		if len(users) != 0:
			return HttpResponse(render(request, "form_signup.html", {"message":"USEREXISTS"}))
		try:
			userCreation = User.objects.create_user(username, email, password)
			# if current_user is the first user of the app then making him/her admin
			c.execute("SELECT COUNT(*) FROM account")
			num_of_user = c.fetchone()
			if num_of_user[0] == 0:
				c.execute('UPDATE auth_user SET is_superuser = 1 WHERE username = "%s"' % (username))
				c.execute('UPDATE auth_user SET is_staff = 1 WHERE username = "%s"' % (username))
			activation_code = get_random_string(30)
			c.execute('INSERT INTO account(Username, phone_number, activation_code) VALUES("%s", "%s", "%s")' % (username, phone_number, activation_code))
			# now we need to send a email activation link
			message_body = "Hello " + username + ", Please find the activation link : \n"
			message_body += "http://127.0.0.1:8000/activation/?code=" + activation_code
			send_mail("Welcome to RailHelp", message_body, 'nicebharat00@gmail.com', [email])
			print("success")
			return render(request, "home.html", {"message":"SUCCESS"})
		except Exception as e:
			return HttpResponse(render(request,"form_signup.html", {"message":"FAILURE"}))
		finally:
			connection.close()
	else:
		return HttpResponse(render(request, "form_signup.html"))

def activation(request):
	if request.method == "GET":
		code = request.GET['code']
		c = connection.cursor()
		try:
			c.execute('UPDATE account SET enabled = "%s" WHERE activation_code = "%s"' % ('Y', code))
			return HttpResponseRedirect("/login/")
		except Exception as e:
			return HttpResponseRedirect("/home/")
		finally:
			connection.close()
	else:
		return HttpResponse(render(request, "form_login.html", {"message":"POSTMETHOD"}))

def login_user(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/dashboard/")
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		c = connection.cursor()
		c.execute('SELECT * FROM account WHERE Username="%s"' % (username))
		f = c.fetchone()
		if f == None:
			return HttpResponse(render(request, "form_login.html", {"message":"FAILED"}))
		if f[4] == 'Y':
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return HttpResponseRedirect("/dashboard/")
			else:
				return HttpResponse(render(request, "form_login.html", {"message":"FAILED"}))
		else:
			return HttpResponse(render(request, "form_login.html", {"message":"NOPERMISSION"}))
	return HttpResponse(render(request, "form_login.html", {"message":"NULL"}))

def list_trains(request):
	c=connection.cursor()
	tif=[]
	c.execute('SELECT * FROM Train')
	for row in c.fetchall():
		s = str(row[0]) + " : " + row[1]
		tif.insert(0,s)

	context = {'traininfo':tif}
	return HttpResponse(render(request,"list_trains.html",context))

def list_stations(request):
	c=connection.cursor()
	tif=[]
	c.execute('SELECT * FROM Station')
	for row in c.fetchall():
		s = str(row[0]) + " : " + row[1]
		tif.insert(0,s)
	context = {'stationinfo':tif}
	return HttpResponse(render(request,"list_stations.html",context))

@login_required
def add_train(request):
	if request.user.is_superuser:
		if request.method=="POST":
			trainno=request.POST.get("trainno")
			trainname = request.POST.get("trainname")
			seatsleeper = request.POST.get("seatsleeper")
			seatfirst = request.POST.get("seatfirst")
			seatsecond = request.POST.get("seatsecond")
			seatthird = request.POST.get("seatthird")
			c = connection.cursor()
			count = 0
			c.execute("SELECT * FROM Train where Train_No='%s' " %(trainno))
			for row in c.fetchall():
				count=count+1
			if count == 0:
				c.execute('''INSERT INTO Train(Train_No,Name,Seat_Sleeper,Seat_First_Class_AC,Seat_Second_Class_AC,Seat_Third_Class_AC) VALUES ("%s","%s","%s","%s","%s","%s")''' %(trainno,trainname,seatsleeper,seatfirst,seatsecond,seatthird) )
				return HttpResponseRedirect("/dashboard/")
			else :
				return HttpResponseRedirect("/dashboard/")
		return HttpResponse(render(request,"add_trains.html"))
	else:
		return HttpResponseRedirect("/dashboard/")

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/home/")

@login_required
def write_feedback(request):
	if request.method == "POST":
		feedbackheading = request.POST.get("fhead")
		feedbacktext = request.POST.get("ftext")
		username = request.user.username
		c =connection.cursor()
		c.execute('INSERT INTO Feedback(Feedback_heading,Feedback_text,Username) VALUES ("%s","%s","%s")' %(feedbackheading,feedbacktext,username))
		return HttpResponse(render(request,"write_feedback.html",{"done":True}))
	return HttpResponse(render(request,"write_feedback.html",{"done":False}))

@login_required
def show_feedback(request):
	if request.user.is_superuser:
		c = connection.cursor()
		c.execute('SELECT * FROM Feedback')
		feedbacks = c.fetchall()
		lst = []
		for i in feedbacks:
			s = str(i[1])+ " : " + str(i[2]) + " - by " + str(i[3])
			lst.insert(0,s)
		return HttpResponse(render(request,"list_feedback.html",{"feedback":lst}))
	return HttpResponseRedirect("/dashboard/")

@login_required
def profile_page(request):
	username=request.user
	c = connection.cursor()
	c.execute('SELECT * FROM account WHERE Username="%s" ' %(username))
	# checking whether the given user exists or not
	flag = c.fetchall()
	if len(flag) == 0:
		return HttpResponse(render(request,"profile_page.html",{"msg":True}))
	c.execute('SELECT * FROM account WHERE Username="%s" ' %(username))
	account_usr = c.fetchone()
	c.execute('SELECT * FROM auth_user WHERE Username="%s" ' %(username))
	auth_user_usr = c.fetchone()
	return HttpResponse(render(request,"profile_page.html",{"userf":account_usr,"users":auth_user_usr,"msg":False}))

@login_required
def edit_profile(request):
	c = connection.cursor()
	if request.method=="POST":
		name = request.POST.get("name")
		phn = request.POST.get("phone")
		address = request.POST.get("address")
		print(name)
		username = request.user.username
		c.execute('''UPDATE account set Name = "%s" WHERE Username  = "%s"
				         ''' %(name, username))
		c.execute('''UPDATE account set phone_number = "%s" WHERE Username  = "%s"
				         ''' %(phn, username))
		c.execute('''UPDATE account set Location = "%s" WHERE Username  = "%s"
				         ''' %(address, username))

	c.execute('SELECT * FROM account WHERE Username="%s" ' %(request.user.username))
	user = c.fetchone()
	return HttpResponse(render(request,"edit_profile.html",{"userf":user}))