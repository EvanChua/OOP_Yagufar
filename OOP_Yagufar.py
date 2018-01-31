from flask import Flask, render_template, request, session, flash, request, url_for, redirect, current_app
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, IntegerField, ValidationError, TextField, validators, FileField
# from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators, IntegerField
import firebase_admin
from firebase_admin import credentials, db
from Storage import Storage
from Repair import Repair
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, validators, FileField,TextField, \
    ValidationError, IntegerField
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
    blocknumber = IntegerField('Block Number: ', [validators.DataRequired(),RequiredIf(cORd='customer')])
    unitnumber = IntegerField('Unit Number: ', [validators.DataRequired(),RequiredIf(cORd='customer')])
    lockerId = StringField('Locker ID: ', [RequiredIf(cORd='deliveryman')])
    dateofdelivery = StringField('Date Of Delivery: ', [RequiredIf(cORd='deliveryman')])

# class StorageForm2(Form):



class RegisterForm(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    name = StringField('Name: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ', [validators.Length(min=1,max=100),validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password: ')
    email_address = TextField('Email Address : ',[validators.Length(min=1,max=100),validators.Email() , validators.DataRequired()])
    block = StringField('BLock Number: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    unit = StringField('Unit : ',[validators.DataRequired()])
    phone_number = StringField('Phone Number: ',[validators.Length(min=8,max=8),validators.DataRequired()])
    type = 'R'

class RegisterForm_Technician(Form):
    username = StringField('Username: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    name = StringField('Name: ',[validators.Length(min=1,max=100),validators.DataRequired()])
    password = PasswordField('Password: ', [validators.Length(min=1,max=100),validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password: ')
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


# class profileForm(Form):
#     profile_pic = FileField()
#     profile_desc = TextAreaField('Description')

class editForm(Form):
    username = StringField('Username : ')
    password = PasswordField('Password : ')
    email_address = StringField('Email Address : ', [validators.DataRequired(),validators.Email()])
    phone_number = StringField('Phone Number : ', [validators.DataRequired()])
    profile_pic = StringField("Profile picture(URL) : ")
    profile_desc = TextAreaField("Description : ")
    name = StringField("Name : ")
    block = StringField("Block : ")
    unit = IntegerField("Unit : ")
    type = StringField("Type : ")

class editFormTech(Form):
    username = StringField('Username : ')
    name = StringField('Name : ')
    password = PasswordField('Password : ')
    email_address = StringField('Email Address : ', [validators.DataRequired(),validators.Email()])
    phone_number = StringField('Phone Number : ', [validators.DataRequired()])
    profile_pic = StringField("Company picture(URL) : ")
    profile_desc = TextAreaField("Description : ")
    postal = StringField("Postal : ")
    address = StringField("Address : ")
    occupation = StringField("Occupation : ")
    companyname = StringField("Company name : ")
    type = StringField("Type : ")

class changePassword(Form):
    oldpassword = PasswordField('Current Password : ', [validators.DataRequired()])
    newpassword = PasswordField('New Password : ', [validators.DataRequired()])
    confirmpassword = PasswordField('Confirm New Password : ', [validators.DataRequired()])

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
            blocknumber = form.blocknumber.data
            unitnumber = form.unitnumber.data

            c = customer(recipientName, blocknumber, unitnumber)
            customer_db = root.child('customer')
            customer_db.push({
                'recipientName': c.get_recipientName(),
                'blocknumber': c.get_blocknumber(),
                'unitnumber': c.get_unitnumber(),
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

@app.route('/Register2/', methods=['GET', 'POST'])
def Register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        email_address = form.email_address.data

        ifUserExists = root.child('user').order_by_child('email_address').equal_to(email_address).get()

        if len(ifUserExists)> 0:
            flash('User Exist', 'danger')
            return redirect(url_for('Register'))
        else:
            username = form.username.data
            name = form.name.data
            password = form.password.data
            email_address = form.email_address.data
            phone_number = form.phone_number.data
            block = form.block.data
            unit = form.unit.data
            profile_pic = "http://i0.kym-cdn.com/entries/icons/original/000/025/067/ugandanknuck.jpg"
            profile_desc = "Do you know da wae?"
            type = form.type
            s1 = Users(username, name, password,phone_number, email_address ,  profile_pic, profile_desc,block, unit , type)

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

@app.route('/Register_Technician2/', methods=['GET', 'POST'])
def Register_Technician():
    form = RegisterForm_Technician(request.form)
    if request.method == 'POST' and form.validate():
        email_address = form.email_address.data

        ifUserExists = root.child('Technician_Register').order_by_child('email_address').equal_to(email_address).get()

        if len(ifUserExists) > 0:
            flash('User Exist', 'danger')
            return redirect(url_for('Register'))
        else:
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

@app.route('/Log_In2/',  methods=['GET', 'POST'])
def Log_In():

    form = Log_InForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        type = form.type.data

        if type == 'R':
            ifUserExists = root.child('user').order_by_child('username').equal_to(username).get()
            if len(ifUserExists) <= 0:

                error = 'Wrong Username or Password '
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
                        session["password"] = password
                        return redirect(url_for('home'))
                    else:
                        error = 'Wrong Username or Password '
                        flash(error, 'danger')
                        return render_template('Log_In2.html', form=form)

        elif type == 'T':
            ifUserExists = root.child('Technician_Register').order_by_child('username').equal_to(username).get()
            if len(ifUserExists) <= 0:

                error = 'Wrong Username or Password '
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
                        session["password"] = password
                        return redirect(url_for('home'))
                    else:
                        error = 'Wrong Username or Password '
                        flash(error, 'danger')
                        return render_template('Log_In2.html', form=form)
        else:
            error = 'Wrong Username or Password '
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
        print(eachvalue)

        info = Users(eachvalue["username"], eachvalue["name"], eachvalue["password"], eachvalue["phone_number"], eachvalue["email_address"], eachvalue["profile_pic"], eachvalue["profile_desc"], eachvalue["block"], eachvalue["unit"],  eachvalue["type"])
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




@app.route('/Service_Profile/',  methods=['GET', 'POST'])
def Service_Profile():
    # form = profileForm(request.form)
    details = root.child("Technician_Register").get()
    list = []
    for values in details:
        eachvalue = details[values]
        print(eachvalue)

        info = technician(eachvalue["username"], eachvalue["name"], eachvalue["password"], eachvalue["phone_number"],
                          eachvalue["email_address"], eachvalue["address"], eachvalue["occupation"],
                          eachvalue["companyname"], eachvalue["type"],  eachvalue["postal"],  eachvalue["profile_pic"],  eachvalue["profile_desc"])
        info.set_profileid(values)
        list.append(info)
    print(list)
    return render_template('Service_Profile.html', details=list)


@app.route("/Edit_Profile/<string:id>", methods=['GET', 'POST'])
def Edit(id):
    form = editForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        name = form.name.data
        password = form.password.data
        phone_number = form.phone_number.data
        email_address = form.email_address.data
        profile_pic = form.profile_pic.data
        profile_desc = form.profile_desc.data
        block = form.block.data
        unit = form.unit.data
        type = form.type.data

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', "danger")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
        image = '../static/img/' + file.filename
        print(image)
        # justey = root.child('user').order_by_child('username').equal_to(session["username"]).get()
        # for k, v in justey.items():
        #     username = v["username"]
        #     password = v["password"]

        variable = Users(username, name, password,phone_number, email_address ,  profile_pic, profile_desc,block, unit , type)

        bobo_db = root.child("user/" + id)
        bobo_db.set({
            "username":session["username"],
            "name":variable.get_name(),
            "password":session["password"],
            "phone_number":variable.get_phone_number(),
            "email_address":variable.get_email_address(),
            "profile_pic":image,
            "profile_desc":variable.get_profile_desc(),
            "block":variable.get_block(),
            "unit":variable.get_unit(),
            "type":variable.get_type(),

            })

        flash("Changes successfully updated","success")

        return redirect(url_for("Profile"))

    else:
        url = "user/" +id
        eachprofile = root.child(url).get()

        edits = Users(eachprofile["username"],eachprofile["name"],eachprofile["password"],eachprofile["phone_number"],eachprofile["email_address"],eachprofile["profile_pic"],eachprofile["profile_desc"],eachprofile["block"],eachprofile["unit"],eachprofile["type"])

        edits.set_profileid(id)
        form.username.data = edits.get_username()
        form.password.data = edits.get_password()
        form.phone_number.data = edits.get_phone_number()
        form.email_address.data = edits.get_email_address()
        form.profile_pic.data = edits.get_profile_pic()
        form.profile_desc.data = edits.get_profile_desc()
        form.name.data = edits.get_name()
        form.block.data = edits.get_block()
        form.unit.data = edits.get_unit()

    return render_template("Edit_Profile.html" , form=form)






@app.route("/Edit_Company_Details/<string:id>", methods=['GET', 'POST'])
def EditTechnician(id):
    form = editFormTech(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        name = form.name.data
        password = form.password.data
        phone_number = form.phone_number.data
        email_address = form.email_address.data
        address = form.address.data
        occupation = form.occupation.data
        companyname = form.companyname.data
        postal = form.postal.data
        profile_pic = form.profile_pic.data
        profile_desc = form.profile_desc.data
        type = form.type.data


        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', "danger")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
        image = '../static/img/' + file.filename
        print(image)
        # justey = root.child('user').order_by_child('username').equal_to(session["username"]).get()
        # for k, v in justey.items():
        #     username = v["username"]
        #     password = v["password"]

        variable = technician(username, name, password, phone_number, email_address, address, occupation, companyname,
                              type, postal, profile_pic, profile_desc)

        bobo_db = root.child("Technician_Register/" + id)
        bobo_db.set({
            "username":session["username"],
            "name":variable.get_name(),
            "password":session["password"],
            "phone_number":variable.get_phone_number(),
            "email_address":variable.get_email_address(),
            "address":variable.get_address(),
            "occupation": variable.get_occupation(),
            "companyname": variable.get_companyname(),
            "type": variable.get_type(),
            "postal": variable.get_postal(),
            "profile_pic":image,
            "profile_desc":variable.get_profile_desc(),


            })

        flash("Changes successfully updated","success")

        return redirect(url_for("Service_Profile"))

    else:
        url = "Technician_Register/" +id
        eachprofile = root.child(url).get()

        edits = technician(eachprofile["username"],eachprofile["name"],eachprofile["password"],
                           eachprofile["phone_number"],eachprofile["email_address"],eachprofile["address"],
                           eachprofile["occupation"],eachprofile["companyname"],eachprofile["type"],
                           eachprofile["postal"],eachprofile["profile_pic"],eachprofile["profile_desc"])

        edits.set_profileid(id)
        form.username.data = edits.get_username()
        form.password.data = edits.get_password()
        form.phone_number.data = edits.get_phone_number()
        form.email_address.data = edits.get_email_address()
        form.profile_pic.data = edits.get_profile_pic()
        form.profile_desc.data = edits.get_profile_desc()
        form.name.data = edits.get_name()
        form.occupation.data = edits.get_occupation()
        form.companyname.data = edits.get_companyname()
        form.postal.data = edits.get_postal()
        form.address.data = edits.get_address()

    return render_template("Edit_Company_Details.html" , form=form)








@app.route("/Change_Password/<string:id>", methods=['GET', 'POST'])
def ChangePassword(id):
    form = changePassword(request.form)
    if request.method == 'POST' and form.validate():
        try:
            if session["logged_in"] == True:
                url = "user/" + id
                eachprofile = root.child(url).get()

                edits = Users(eachprofile["username"],eachprofile["name"], eachprofile["password"], eachprofile["phone_number"],
                              eachprofile["email_address"], eachprofile["profile_pic"], eachprofile["profile_desc"], eachprofile["block"], eachprofile["unit"],eachprofile["type"])
                phone_number = edits.get_phone_number()
                email_address = edits.get_email_address()
                image = edits.get_profile_pic()
                profile_desc = edits.get_profile_desc()
                name = edits.get_name()
                block = edits.get_block()
                unit = edits.get_unit()
                type = edits.get_type()

                oldpassword = form.oldpassword.data
                newpassword = form.newpassword.data
                confirmpassword = form.confirmpassword.data

                if oldpassword == session["password"]:
                    if newpassword == confirmpassword:
                        if confirmpassword != oldpassword:
                            username = session["username"]
                            password = confirmpassword
                            session["password"] = confirmpassword

                            bobo_db = root.child("user/" + id)
                            bobo_db.set({
                                "username": username,
                                "name": name,
                                "password": password,
                                "phone_number": phone_number,
                                "email_address":email_address,
                                "profile_pic": image,
                                "profile_desc":profile_desc,
                                "block":block,
                                "unit":unit,
                                "type":type,


                            })

                            flash("Password successfully updated", "success")
                            return redirect(url_for("Profile"))
                        else:
                            flash("Password must differ from old password!", "danger")
                    else:
                        error = 'New Password and Confirm Password does not match'
                        flash(error, 'danger')
                else:
                    error = 'Current Password is incorrect'
                    flash(error, 'danger')
        except:
            if session["logged_in_technician"] == True:
                url = "Technician_Register/" + id
                eachvalue= root.child(url).get()

                edits = technician(eachvalue["username"], eachvalue["name"], eachvalue["password"],
                                  eachvalue["phone_number"],
                                  eachvalue["email_address"], eachvalue["address"], eachvalue["occupation"],
                                  eachvalue["companyname"], eachvalue["type"], eachvalue["postal"],
                                  eachvalue["profile_pic"], eachvalue["profile_desc"])

                phone_number = edits.get_phone_number()
                email_address = edits.get_email_address()
                image = edits.get_profile_pic()
                profile_desc = edits.get_profile_desc()
                name = edits.get_name()
                address = edits.get_address()
                companyname = edits.get_companyname()
                occupation = edits.get_occupation()
                postal = edits.get_postal()
                type = edits.get_type()

                oldpassword = form.oldpassword.data
                newpassword = form.newpassword.data
                confirmpassword = form.confirmpassword.data

                if oldpassword == session["password"]:
                    if newpassword == confirmpassword:
                        if confirmpassword != oldpassword:
                            username = session["username"]
                            password = confirmpassword
                            session["password"] = confirmpassword

                            bobo_db = root.child("Technician_Register/" + id)
                            bobo_db.set({
                                "username": username,
                                "name": name,
                                "password": password,
                                "phone_number": phone_number,
                                "email_address": email_address,
                                "profile_pic": image,
                                "profile_desc": profile_desc,
                                "address":address,
                                "companyname":companyname,
                                "occupation":occupation,
                                "postal":postal,
                                "type": type,

                            })

                            flash("Password successfully updated", "success")
                            return redirect(url_for("Service_Profile"))
                        else:
                            flash("Password must differ from old password!", "danger")
                    else:
                        error = 'New Password and Confirm Password does not match'
                        flash(error, 'danger')
                else:
                    error = 'Current Password is incorrect'
                    flash(error, 'danger')

    return render_template('Change_Password.html', form=form)


@app.route('/Log_Out/')
def Log_Out():
    session.clear()
    flash('Log Out Successful','success')
    return redirect(url_for('Log_In'))

@app.route('/Repair2/')
def viewTechnicians():
    technicians = root.child('Technician_Register').get()
    list = []

    for profileid in technicians:

        eachtechnicians = technicians[profileid]

        worker = technician(eachtechnicians['username'], eachtechnicians['name'], eachtechnicians['password'], eachtechnicians['phone_number'], eachtechnicians['email_address'], eachtechnicians['address'], eachtechnicians['occupation'], eachtechnicians['companyname'])
        worker.set_profileid(profileid)
        print(worker.get_profileid())
        print(worker.get_address())
        list.append(worker)

    return render_template('Repair2.html', technicians = list)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(port="80")

