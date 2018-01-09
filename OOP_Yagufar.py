from flask import Flask, render_template, request, session, flash, request, url_for, redirect
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators, IntegerField
import firebase_admin
from firebase_admin import credentials, db
from Storage import Storage
from Repair import Repair
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators, FileField, \
    ValidationError, IntegerField
from Users import Users
from Review import Review
from Profile import Profile

app = Flask(__name__)
cred = credentials.Certificate('cred/yagufar-bb205-firebase-adminsdk-p7ypj-a0ee653a2d.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://yagufar-bb205.firebaseio.com/'

})

root = db.reference()


class StorageForm(Form):
    recipientName = StringField('Recipent Name: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    lockerId = StringField('Locker ID: ',[validators.DataRequired()])
    dateofdelivery = StringField('Date Of Delivery: ',[validators.DataRequired()])
    phonenumber = IntegerField('Phone Number: ',[validators.DataRequired()])
    emailaddress = StringField('Email Address: ',[validators.DataRequired()])


class RegisterForm(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])
    email_address = StringField('Email Address : ',[validators.DataRequired()])
    phone_number = StringField('Phone Number: ',[validators.DataRequired()])


class Log_InForm(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired()])


class reviewForm(Form):
    stars = RadioField('Rating', choices=[('1', ""), ("2", ""), ("3", ""), ("4", ""), ("5", "")])
    review = TextAreaField('Review', [validators.DataRequired()])


class profileForm(Form):
    profile_pic = FileField()
    profile_desc = TextAreaField('Description')



class RepairForm(Form):
    chooseService = SelectField('Select A Service', [validators.DataRequired()],
                                choices=[('', 'Select Here'), ('AIRCON','Air Conditioning'), ('PLUMB', 'Plumbing')],
                                default='')
    chooseLocation = TextAreaField('Select A Location', [validators.DataRequired()])
    chooseQuest = TextAreaField('Have Any Special Request?(Leave empty if not needed')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/home/')
def home1():
    return render_template('home.html')


@app.route('/storage2/')
def storage2():
    return render_template('storage2.html')

@app.route('/Storage/',  methods=['GET', 'POST'])
def storage_item():
    form = StorageForm(request.form)
    if request.method == 'POST' and form.validate():
        recipientName = form.recipientName.data
        lockerId = form.lockerId.data
        dateofdelivery = form.dateofdelivery.data
        phonenumber = form.phonenumber.data
        emailaddress = form.emailaddress.data
        s1 = Storage(recipientName, lockerId, dateofdelivery, phonenumber, emailaddress)

        # create the magazine object
        mag_db = root.child('storage')
        mag_db.push({
            'recipientName': s1.get_recipientName(),
            'lockerId': s1.get_lockerId(),
            'dateofdelivery': s1.get_dateofdelivery(),
            'phonenumber': s1.get_phonenumber(),
            'emailaddress': s1.get_emailaddress(),

        })
        return redirect(url_for('storage2'))

        #return render_template('Storage.html', form=form)
    return render_template('Storage.html', form=form)

@app.route('/Repair/', methods=['GET','POST'])
def Repair():
    if request.method == 'POST' and Form.validate():
        return render_template('Repair.html')
    return render_template('Repair.html')

@app.route('/Register/', methods=['GET', 'POST'])
def Register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        email_address = form.email_address.data
        phone_number = form.phone_number.data
        profile_pic = "data:image/jpeg;base64,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"
        profile_desc = "HI PEEPS"
        s1 = Users(username, password, phone_number, email_address)

    # create the magazine object
        mag_db = root.child('user')
        mag_db.push({
            'username': s1.get_username(),
            'password': s1.get_password(),
            'phone_number': s1.get_phone_number(),
            'email_address': s1.get_email_address(),
            'profile_pic' : profile_pic,
            'profile_desc' : profile_desc,





        })
        return redirect(url_for('Log_In'))

    return render_template('Register.html', form=form)


@app.route('/Repair/', methods=['GET', 'POST'])
def repair_services():
    form = RepairForm(request.form)
    if request.method == 'POST' and form.validate():
        service = form.chooseService.data
        location = form.chooseLocation.data
        quest = form.chooseQuest.data
        s1 = Repair(service, location, quest)

        # create the magazine object
        mag_db = root.child('repair')
        mag_db.push({
            'service': s1.get_chooseService(),
            'location': s1.get_chooseLocation(),
            'request': s1.get_chooseQuest(),

        })
        return redirect(url_for('confirm.html'))

    return render_template('Repair.html', form=form)


@app.route('/Log_In/', methods=['GET', 'POST'])
def Log_In():

    form = Log_InForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        ifUserExists = root.child('user').order_by_child('username').equal_to(username).get()
        if len(ifUserExists) <= 0:

            error = 'Invalid login'
            flash(error, 'danger')
            return render_template('Log_In.html', form=form)
        else:
            for k, v in ifUserExists.items():
                print(k, v)
                # print(sha256_crypt.encrypt(password))
                print(v['username'])
                print(v['password'])

                if username == v['username'] and password == v['password']:
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('home'))
                else:
                    error = 'Invalid login'
                    flash(error, 'danger')
                    return render_template('Log_In.html', form=form)


    return render_template('Log_In.html', form=form)



@app.route('/Review/',  methods=['GET', 'POST'])
def render_review():
    form = reviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = form.review.data
        s1 = Review(review)
        mag_db = root.child("review")
        mag_db.push({
            'review': s1.get_review(),

        })
        return redirect(url_for('Profile'))


    return render_template('Review.html', form=form)



@app.route('/Profile/',  methods=['GET', 'POST'])
def Profile():
    # form = profileForm(request.form)
    details = root.child("user").get()
    list = []
    for values in details:
        eachvalue = details[values]

        info = Users(eachvalue["username"], eachvalue["password"], eachvalue["phone_number"], eachvalue["email_address"])
        # info.set_boboid(values)
        list.append(info)
    return render_template('Profile.html', details=details)

def ProfilePicture():
    form = profileForm(request.form)
    if request.method == "POST" and form.validate():
        profile_pic = form.profile.data
        s1 = Profile(profile_pic)
        mag_db = root.child("user")
        mag_db.push({
            'profile_pic': s1.get_profile_pic(),

        })

def ProfileDescription():
    form = profileForm(request.form)
    if request.method == "POST" and form.validate():
        profile_desc = form.profile.data
        s1 = Profile(profile_desc)
        mag_db = root.child("user")
        mag_db.push({
            'profile_desc': s1.get_profile_desc(),

        })


    return render_template('Profile.html', details = list)


@app.route('/Log_Out/')
def Log_Out():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('Log_In'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(port="80")

