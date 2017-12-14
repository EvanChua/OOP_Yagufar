from flask import Flask, render_template, request, url_for, redirect
import firebase_admin
from firebase_admin import credentials, db
from Storage import Storage
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators, ValidationError,IntegerField
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


@app.route('/home/')
def home():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)
