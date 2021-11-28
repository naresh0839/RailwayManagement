# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    username = models.CharField(db_column='Username', primary_key=True, max_length=15)  # Field name made lowercase.
    email_id = models.CharField(db_column='Email_Id', max_length=35)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Contact(models.Model):
    username = models.OneToOneField(Account, models.DO_NOTHING, db_column='Username', primary_key=True)  # Field name made lowercase.
    phone_no = models.CharField(db_column='Phone_No', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contact'
        unique_together = (('username', 'phone_no'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Feedback(models.Model):
    feedback_id = models.AutoField(db_column='Feedback_id', primary_key=True)  # Field name made lowercase.
    feedback_heading = models.CharField(db_column='Feedback_heading', max_length=1000)  # Field name made lowercase.
    feedback_text = models.CharField(db_column='Feedback_text', max_length=1000)  # Field name made lowercase.
    username = models.ForeignKey(Account, models.DO_NOTHING, db_column='Username')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'feedback'


class Passenger(models.Model):
    passenger_id = models.AutoField(db_column='Passenger_Id', primary_key=True)  # Field name made lowercase.
    first_name = models.CharField(db_column='First_Name', max_length=20)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=20)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1)  # Field name made lowercase.
    phone_no = models.CharField(db_column='Phone_No', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ticket_no = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='Ticket_No')  # Field name made lowercase.
    age = models.IntegerField(db_column='Age')  # Field name made lowercase.
    class_field = models.CharField(db_column='Class', max_length=20)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'passenger'


class Seats(models.Model):
    train_no = models.OneToOneField('Train', models.DO_NOTHING, db_column='Train_No', primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    seat_sleeper = models.IntegerField(db_column='Seat_Sleeper')  # Field name made lowercase.
    seat_first_class_ac = models.IntegerField(db_column='Seat_First_Class_AC')  # Field name made lowercase.
    seat_second_class_ac = models.IntegerField(db_column='Seat_Second_Class_AC')  # Field name made lowercase.
    seat_third_class_ac = models.IntegerField(db_column='Seat_Third_Class_AC')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seats'
        unique_together = (('train_no', 'date'),)


class Station(models.Model):
    station_code = models.CharField(db_column='Station_Code', primary_key=True, max_length=5)  # Field name made lowercase.
    station_name = models.CharField(db_column='Station_Name', max_length=25)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'station'


class Stoppage(models.Model):
    train_no = models.OneToOneField('Train', models.DO_NOTHING, db_column='Train_No', primary_key=True)  # Field name made lowercase.
    station_code = models.ForeignKey(Station, models.DO_NOTHING, db_column='Station_Code')  # Field name made lowercase.
    arrival_time = models.TimeField(db_column='Arrival_Time', blank=True, null=True)  # Field name made lowercase.
    departure_time = models.TimeField(db_column='Departure_Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stoppage'
        unique_together = (('train_no', 'station_code'),)


class Ticket(models.Model):
    ticket_no = models.AutoField(db_column='Ticket_No', primary_key=True)  # Field name made lowercase.
    train_no = models.ForeignKey('Train', models.DO_NOTHING, db_column='Train_No')  # Field name made lowercase.
    date_of_journey = models.DateField(db_column='Date_of_Journey')  # Field name made lowercase.
    username = models.ForeignKey(Account, models.DO_NOTHING, db_column='Username')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ticket'


class Train(models.Model):
    train_no = models.IntegerField(db_column='Train_No', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=25)  # Field name made lowercase.
    seat_sleeper = models.IntegerField(db_column='Seat_Sleeper')  # Field name made lowercase.
    seat_first_class_ac = models.IntegerField(db_column='Seat_First_Class_AC')  # Field name made lowercase.
    seat_second_class_ac = models.IntegerField(db_column='Seat_Second_Class_AC')  # Field name made lowercase.
    seat_third_class_ac = models.IntegerField(db_column='Seat_Third_Class_AC')  # Field name made lowercase.
    wifi = models.CharField(db_column='Wifi', max_length=1)  # Field name made lowercase.
    food = models.CharField(db_column='Food', max_length=1)  # Field name made lowercase.
    run_on_sunday = models.CharField(db_column='Run_On_Sunday', max_length=1)  # Field name made lowercase.
    run_on_monday = models.CharField(db_column='Run_On_Monday', max_length=1)  # Field name made lowercase.
    run_on_tuesday = models.CharField(db_column='Run_On_Tuesday', max_length=1)  # Field name made lowercase.
    run_on_wednesday = models.CharField(db_column='Run_On_Wednesday', max_length=1)  # Field name made lowercase.
    run_on_thursday = models.CharField(db_column='Run_On_Thursday', max_length=1)  # Field name made lowercase.
    run_on_friday = models.CharField(db_column='Run_On_Friday', max_length=1)  # Field name made lowercase.
    run_on_saturday = models.CharField(db_column='Run_On_Saturday', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'train'
