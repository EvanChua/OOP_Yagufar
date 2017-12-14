from flask import Flask, render_template, request
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators
import firebase_admin
from firebase_admin import credentials, db
from Storage import Storage
app = Flask(__name__)
cred = credentials.Certificate('cred/yagufar-bb205-firebase-adminsdk-p7ypj-a0ee653a2d.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://yagufar-bb205.firebaseio.com/'

})

root = db.reference()

class StorageForm(Form):
    recipientName = StringField('Recipent Name: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    lockerId = StringField('Locker ID: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    dateofdelivery = StringField('Date Of Delivery: ',[validators.DataRequired()])
    phonenumber = StringField('Phone Number: ',[validators.DataRequired()])

class RegisterForm(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    Password = PasswordField('Password: ', [validators.DataRequired()])
    email_address = StringField('Email Address : ',[validators.DataRequired()])
    phone_number = StringField('Phone Number: ',[validators.DataRequired()])

class Log_InForm(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    Password = PasswordField('Password: ',[validators.DataRequired()])


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

@app.route('/Repair/')
def Repair():
    return render_template('Repair.html')

@app.route('/Register/', methods=['GET', 'POST'])
def Register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        Password = form.Password.data
        Email_Address = form.Email_address.data
        phone_number = form.phone_number.data
        s1 = Users(username, Password, Email_Address, phone_number)
        return render_template('Register.html', form=form)

    # create the magazine object
        mag_db = root.child('user')
        mag_db.push({
            'username': s1.get_username(),
            'password': s1.get_password(),
            'phone_number': s1.get_phone_number(),
            'email_address': s1.get_email_address(),

        })
        return redirect(url_for('Log_In.html'))

    return render_template('Register.html', form=form)

@app.route('/Log_In/',  methods=['GET', 'POST'])
def Log_In():
    form = Log_InForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template('Log_In.html', form=form)
    return render_template('Log_In.html', form=form)

@app.route('/Review/')
def Review():
    return render_template('Review.html')

if __name__ == '__main__':
    app.run(debug=True)
