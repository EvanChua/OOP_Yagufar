from flask import Flask, render_template, request, session, flash, request, url_for, redirect, current_app
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, IntegerField, ValidationError, TextField, validators, FileField
# from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators, IntegerField
import firebase_admin
from firebase_admin import credentials, db
from Storage import Storage,deliveryman,customer
from Users import Users
from Repair import Repair
from technician import technician
from Review import Review
from Profile import Profile
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




cred = credentials.Certificate('cred/yagufar-bb205-firebase-adminsdk-p7ypj-a0ee653a2d.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://yagufar-bb205.firebaseio.com/'

})

root = db.reference()
class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)


# class UniqueUser(object):
#     def __init__(self, message="User exists"):
#         self.message = message
#
#     def __call__(self, form, field):
#         if current_app.security.datastore.find_user(email=field.data):
#             raise ValidationError(self.message)
#
# validators = {
#     'email': [
#         Required(),
#         Email(),
#         UniqueUser(message='Email address is associated with '
#                            'an existing account')
#     ],
#     'password': [
#         Required(),
#         Length(min=6, max=50),
#         EqualTo('confirm', message='Passwords must match'),
#         Regexp(r'[A-Za-z0-9@#$%^&+=]',
#                message='Password contains invalid characters')
#     ]
# }


class StorageForm(Form):
    cORd = RadioField("Customer or Deliveryman: ", choices=[('customer', 'Customer'), ('deliveryman', 'Deliveryman')],
                      default='')
    recipientName = StringField('Recipient Name: ', [validators.Length(min=1, max=100), validators.DataRequired()])
    phonenumber = IntegerField('Phone Number: ', [validators.DataRequired()])
    emailaddress = StringField('Email Address: ', [validators.DataRequired()])
    lockerId = StringField('Locker ID: ', [RequiredIf(cORd='deliveryman')])
    dateofdelivery = StringField('Date Of Delivery: ', [RequiredIf(cORd='deliveryman')])


class RegisterForm(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    name = StringField('Name: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ', [validators.Length(min=1,max=100),validators.DataRequired()])
    email_address = TextField('Email Address : ',[validators.Length(min=1,max=100),validators.Email() , validators.DataRequired()])
    block = StringField('BLock Number: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    unit = StringField('Unit : ',[validators.DataRequired()])
    phone_number = StringField('Phone Number: ',[validators.Length(min=8,max=8),validators.DataRequired()])
    type = 'R'

class RegisterForm_Technician(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    name = StringField('Name: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ', [validators.Length(min=1,max=100),validators.DataRequired()])
    email_address = StringField('Email Address : ',[validators.Length(min=1,max=100), validators.Email() ,validators.DataRequired()])
    postal = StringField('Postal For Your Company: ',[validators.Length(min=6,max=6),validators.DataRequired()])
    phone_number = StringField('Phone Number: ',[validators.Length(min=8,max=8),validators.DataRequired()])
    occupation = StringField('Occupation: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    companyname = StringField('Company Name: ',[validators.Length(min=1,max=100),validators.DataRequired()] )
    type = 'T'


class Log_InForm(Form):
    type = SelectField('Role', [validators.DataRequired()],
                                choices=[('', 'Select Here'), ('R','Residence'), ('T', 'Technician')],
                                default='')
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired()])


class reviewForm(Form):
    stars = RadioField('Rating', choices=[('1', ""), ("2", ""), ("3", ""), ("4", ""), ("5", "")])
    review = TextAreaField('Review', [validators.DataRequired()])


class profileForm(Form):
    profile_pic = FileField()
    profile_desc = TextAreaField('Description')

class editForm(Form):
    username = StringField('Username : ', [validators.Length(min=1, max=100), validators.DataRequired()])
    password = PasswordField('New Password : ', [validators.DataRequired()])
    email_address = StringField('New Email Address : ', [validators.DataRequired(),validators.Email()])
    phone_number = StringField('New Phone Number : ', [validators.DataRequired()])
    profile_pic = StringField("Change Profile picture(URL) : ")
    profile_desc = TextAreaField("Edit description : ")


class RepairForm(Form):
    chooseService = SelectField('Select A Service', [validators.DataRequired()],
                                choices=[('', 'Select Here'), ('AIRCON','Air Conditioning'), ('PLUMB', 'Plumbing')],
                                default='')
    chooseLocation = TextAreaField('Select A Location', [validators.DataRequired()])
    chooseDate = StringField('Date (year-month-day)',[validators.DataRequired()])
    chooseTime = StringField('Time (hour:minute)',[validators.DataRequired()])
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

@app.route('/storage3/')
def storage3():
    return render_template('storage3.html')

@app.route('/Storage/',  methods=['GET', 'POST'])
def storage_item():
    form = StorageForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.cORd.data == "customer":
            recipientName = form.recipientName.data
            phonenumber = form.phonenumber.data
            emailaddress = form.emailaddress.data

            c = customer(recipientName, phonenumber, emailaddress)
            customer_db = root.child('customer')
            customer_db.push({
                'recipientName': c.get_recipientName(),
                'phonenumber': c.get_phonenumber(),
                'emailaddress': c.get_emailaddress(),
            })
            return redirect(url_for('storage2'))

        elif form.cORd.data == "deliveryman":
            recipientName = form.recipientName.data
            lockerId = form.lockerId.data
            dateofdelivery = form.dateofdelivery.data

            d = deliveryman(recipientName, lockerId, dateofdelivery)
            deliveryman_db = root.child('deliveryman')
            deliveryman_db.push({
                'recipientName': d.get_recipientName(),
                'lockerId': d.get_lockerId(),
                'dateofdelivery': d.get_dateofdelivery(),
            })
            return redirect(url_for('storage3'))
        #return render_template('Storage.html', form=form)
    return render_template('Storage.html', form=form)

@app.route('/Repair/', methods=['GET', 'POST'])
def repair_services():
    form = RepairForm(request.form)
    if request.method == 'POST' and form.validate():
        service = form.chooseService.data
        location = form.chooseLocation.data
        date = form.chooseDate.data
        time = form.chooseTime.data
        quest = form.chooseQuest.data
        s1 = Repair(service, location, date, time, quest)

        # create the magazine object
        mag_db = root.child('repair')
        mag_db.push({
            'service': s1.get_chooseService(),
            'location': s1.get_chooseLocation(),
            'date': s1.get_chooseDate(),
            'time':s1.get_chooseTime(),
            'request': s1.get_chooseQuest(),

        })
        return redirect(url_for('home'))

    return render_template('Repair.html', form=form)

@app.route('/Register/', methods=['GET', 'POST'])
def Register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        email_address = form.email_address.data

        ifUserExists = root.child('user').order_by_child('email_address').equal_to(email_address).get()

        if len(ifUserExists)> 0:
            flash('User Exist')
            return redirect(url_for('Register'))
        else:
            username = form.username.data
            name = form.name.data
            password = form.password.data
            email_address = form.email_address.data
            phone_number = form.phone_number.data
            block = form.block.data
            unit = form.unit.data
            profile_pic = "https://media1.britannica.com/eb-media/58/129958-004-C9B8B89D.jpg"
            profile_desc = "HI PEEPS"
            type = form.type
            s1 = Users(username, name, password,phone_number, email_address , block, unit ,  profile_pic, profile_desc, type)

            # create the magazine object
            mag_db = root.child('user')
            mag_db.push({
                'username': s1.get_username(),
                'name': s1.get_name(),
                'password': s1.get_password(),
                'phone_number': s1.get_phone_number(),
                'email_address': s1.get_email_address(),
                'block': s1.get_block(),
                'unit': s1.get_unit(),
                'profile_pic' : s1.get_profile_pic(),
                'profile_desc' :s1.get_profile_desc(),
                'type': s1.get_type()
            })
            return redirect(url_for('Log_In'))

    return render_template('Register2.html', form=form)

@app.route('/Register_Technician/', methods=['GET', 'POST'])
def Register_Technician():
    form = RegisterForm_Technician(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        name = form.name.data
        password = form.password.data
        email_address = form.email_address.data
        postal = form.postal.data
        phone_number = form.phone_number.data
        occupation = form.occupation.data
        companyname = form.companyname.data
        type = form.type
        s1 = technician(username, name, password, phone_number, email_address, postal , occupation, companyname, type)

        # create the magazine object
        mag_db = root.child('Technician_Register')
        mag_db.push({
             'username': s1.get_username(),
             'name': s1.get_name(),
             'password': s1.get_password(),
             'phone_number': s1.get_phone_number(),
             'email_address': s1.get_email_address(),
             'postal': s1.get_postal(),
             'occupation': s1.get_occupation(),
             'companyname': s1.get_companyname(),
             'type': s1.get_type()
        })
        return redirect(url_for('Log_In2'))

    return render_template('Register_Technician2.html', form=form)

@app.route('/Log_In/',  methods=['GET', 'POST'])
def Log_In():

    form = Log_InForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        type = form.type.data

        if type == 'R':
            ifUserExists = root.child('user').order_by_child('username').equal_to(username).get()
            if len(ifUserExists) <= 0:

                error = 'Invalid login'
                flash(error, 'danger')
                return render_template('Log_In2.html', form=form)
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
                        return render_template('Log_In2.html', form=form)

        elif type == 'T':
            ifUserExists = root.child('Technician_Register').order_by_child('username').equal_to(username).get()
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
                        session['logged_in_technician'] = True
                        session['username'] = username
                        return redirect(url_for('home'))
                    else:
                        error = 'Invalid login'
                        flash(error, 'danger')
                        return render_template('Log_In2.html', form=form)
        else:
            error = 'Invalid login'
            flash(error, 'danger')
            return render_template('Log_In2.html', form=form)


    return render_template('Log_In2.html', form=form)



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

        info = Users(eachvalue["username"], eachvalue["password"], eachvalue["phone_number"], eachvalue["email_address"], eachvalue["profile_pic"], eachvalue["profile_desc"])
        info.set_profileid(values)
        list.append(info)
    print(list)
    return render_template('Profile.html', details=list)

# def ProfilePicture():
#     form = profileForm(request.form)
#     if request.method == "POST" and form.validate():
#         profile_pic = form.profile.data
#         s1 = Profile(profile_pic)
#         mag_db = root.child("user")
#         mag_db.push({
#             'profile_pic': s1.get_profile_pic(),
#
#         })
#
# def ProfileDescription():
#     form = profileForm(request.form)
#     if request.method == "POST" and form.validate():
#         profile_desc = form.profile.data
#         s1 = Profile(profile_desc)
#         mag_db = root.child("user")
#         mag_db.push({
#             'profile_desc': s1.get_profile_desc(),
#
#         })


    # return render_template('Profile.html', details = list)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/Edit_Profile/<string:id>", methods=['GET', 'POST'])
def Edit(id):
    form = editForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        phone_number = form.phone_number.data
        email_address = form.email_address.data
        profile_pic = form.profile_pic.data
        profile_desc = form.profile_desc.data

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
        image = file.filename
        print(image)
        variable = Users(username,password,phone_number,email_address,image,profile_desc)

        bobo_db = root.child("user/" + id)
        bobo_db.set({
            "username":variable.get_username(),
            "password":variable.get_password(),
            "phone_number":variable.get_phone_number(),
            "email_address":variable.get_email_address(),
            "profile_pic":image,
            "profile_desc":variable.get_profile_desc(),

            })

        flash("Changes successfully updated","success")

        return redirect(url_for("Profile"))

    else:
        url = "user/" +id
        eachprofile = root.child(url).get()

        edits = Users(eachprofile["username"],eachprofile["password"],eachprofile["phone_number"],eachprofile["email_address"],eachprofile["profile_pic"],eachprofile["profile_desc"])

        edits.set_profileid(id)
        form.username.data = edits.get_username()
        form.password.data = edits.get_password()
        form.phone_number.data = edits.get_phone_number()
        form.email_address.data = edits.get_email_address()
        form.profile_pic.data = edits.get_profile_pic()
        form.profile_desc.data = edits.get_profile_desc()

    return render_template("Edit_Profile.html" , form=form)




@app.route('/Log_Out/')
def Log_Out():
    session.clear()
    return redirect(url_for('Log_In'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(port="80")

