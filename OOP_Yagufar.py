from flask import Flask, render_template, request
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators
app = Flask(__name__)

class StorageForm(Form):
    recipientName = StringField('Recipent Name: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    lockerId = StringField('Locker ID: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    dateofdelivery = StringField('Date Of Delivery: ',[validators.DataRequired()])
    phonenumber = StringField('Phone Number: ',[validators.DataRequired()])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Storage/',  methods=['GET', 'POST'])
def Storage():
    form = StorageForm(request.form)
    return render_template('Storage.html', form=form)

if __name__ == '__main__':
    app.run()
