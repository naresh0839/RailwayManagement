from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from django.contrib.auth.hashers import make_password,check_password

import MySQLdb

def home(request):
	if request.user.is_authenticated:
		return HttpResponse(render(request,"login_success.html"))
	else:
		return HttpResponse(render(request, "home.html"))

def aboutus(request):
	return HttpResponse(render(request, "aboutus.html"))
	
@login_required
def dashboard(request):
    return HttpResponse(render(request, "login_success.html"))

@login_required
def download_ticket(request):
	if request.method == "POST":
		ticketno = int(request.POST.get('ticketno'))
		c = connection.cursor()
		c.execute('SELECT * FROM Ticket WHERE Ticket_No = %d' %(ticketno))
		tickets = c.fetchone()
		c.execute('SELECT * FROM Passenger WHERE Ticket_No = %d' %(ticketno))
		passenger = c.fetchone()
		context = {"ticket":tickets, "passenger":passenger, "show":True}
		if tickets == None:
			return HttpResponse("Invalid Ticket No!!")
		else:
			return HttpResponse(render(request, "download_ticket.html", context))
	else:
		return HttpResponse(render(request, "download_ticket.html", {"show":False,}))

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
		c.execute('''select a.Train_No from Stoppage as a join Stoppage as b on a.Train_No = b.Train_No 
			         where a.Station_Code = "%s" and b.Station_Code = "%s" ''' %(fstation, sstation))
		
		trains = c.fetchall()
		if len(trains) == 0:
			context = {"show":False, "invalid":True}
			return HttpResponse(render(request, "findtrains.html", context))	

		context = {"trains":trains, "show":True, "invalid":False}

		return HttpResponse(render(request, "findtrains.html", context))
		
	else:
		return HttpResponse(render(request, "findtrains.html", {"show":False,"invalid":False}))	

@login_required
def ticket(request):
	if request.method == "POST":
		tnumber = request.POST.get('tnumber')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		gender = request.POST.get('gender')
		age = request.POST.get('age')
		tclass = request.POST.get('tclass')
		number = request.POST.get('number')

		c = connection.cursor()
		c.execute("SELECT * FROM Train where Train_No = '%s' " %(tnumber))

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
		
		c.execute('''INSERT INTO Ticket VALUES("%s", "%s", "%s", "%s")
					 ''' %(ticketno, tnumber, jdate, request.user))

		c.execute('''INSERT INTO Passenger(First_name, Last_name, Gender, Phone_No,
			         Ticket_No, Age, Class) VALUES
			         ("%s", "%s", "%s", "%s", "%s", "%s", "%s")
			         ''' %(fname, lname, gender, number, ticketno, age, tclass))
        
		if str(tclass) == "sleeper":
			c.execute('''UPDATE Train set Seat_Sleeper = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[2])-1, tnumber))
		if str(tclass) == "first class ac":
			c.execute('''UPDATE Train set Seat_First_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[3])-1, tnumber))
		if str(tclass) == "second class ac":
			c.execute('''UPDATE Train set Seat_Second_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[4])-1, tnumber))
		if str(tclass) == "third class ac":
			c.execute('''UPDATE Train set Seat_Third_Class_AC = "%s" WHERE Train_No = "%s"
				         ''' %(int(train[5])-1, tnumber))			

		context = {"ticket_no":ticketno, "show":True}
		return HttpResponse(render(request, "ticket.html", context))
	else:
		return HttpResponse(render(request, "ticket.html", {"show":False}))	

def signup(request):
	if request.user.is_authenticated:
		return HttpResponse(render(request,"login_success.html"))
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		email = request.POST.get('email')
		address = request.POST.get('address')
		fnumber = request.POST.get('fnumber')
		snumber = request.POST.get('snumber')

		alpha = []
		alp = 'a'
		for i in range(0, 26):
			alpha.append(alp)
			alp = chr(ord(alp) + 1)

		num = []
		zer = '0'
		for i in range(0, 10):
			num.append(zer)
			zer = chr(ord(zer) + 1)

		invalid = False

		if len(username) == 0:
			invalid = True

		for c in username:
			if ((c not in alpha) and (c not in num)):
				invalid = True
				break

		if invalid:
			return HttpResponse("invalid username, characters allowed [a-z] and [0-9]")

		invalid = False

		if len(password) == 0:
			invalid = True

		for c in password:
			if c == " ":
				invalid = True
				break

		if invalid:
			return HttpResponse("space not allowed in the password")

		if len(address) == address.count(' '):
			return HttpResponse("invalid address")

		invalidf, invalids = False, False

		if len(fnumber) != 10:
			invalidf = True

		for c in fnumber:
			if c not in num:
				invalidf = True
				break

		if len(snumber) != 10:
			invalids = True

		for c in snumber:
			if c not in num:
				invalids = True
				break

		if invalids and invalidf:
			print("*")
			return HttpResponse(render(request,"signup_fail.html"))

		try:
			userCreation = User.objects.create_user(username, None, password)
			c = connection.cursor()
			#encodedPass = make_password(password)
			c.execute('INSERT INTO Account VALUES("%s", "%s", "%s")' % (username, email, address))
			if not invalidf:
				c.execute('INSERT INTO Contact VALUES("%s", "%s")' % (username, fnumber))
			if not invalids:
				c.execute('INSERT INTO Contact VALUES("%s", "%s")' % (username, snumber))
			return HttpResponse(render(request, "signup_success.html"))
		except Exception as e:
			print(e)
			return HttpResponse(render(request,"signup_fail.html"))
		finally:
			connection.close()
	else:
		return HttpResponse(render(request, "form_signup.html"))

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(check_password(password,))
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponse(render(request, "login_success.html"))

        else:
            return HttpResponse(render(request, "login_fail.html"))

    if request.user.is_authenticated:
    	return HttpResponse(render(request,"login_success.html"))
    return HttpResponse(render(request, "form_login.html"))

def list_trains(request):
	c=connection.cursor()
	tif=[]
	c.execute('SELECT * FROM Train')
	for row in c.fetchall():
		s = str(row[0]) + " : " + row[1]
		tif.insert(0,s)

	context = {'traininfo':tif}
	return HttpResponse(render(request,"list_trains.html",context))

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/home/")