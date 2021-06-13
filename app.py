from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList
from wtforms.validators import InputRequired, Length, AnyOf, Email
from collections import namedtuple

app = Flask(__name__)
app.debug = True
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = "secret_key_for_token"
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
app.config['SECRET_KEY'] = 'Mysecret!'


class TelephoneForm(Form):
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code')
    number = StringField('Number')


class YearForm(Form):
    year = IntegerField('Year')
    total = IntegerField('Total')


class LoginForm(FlaskForm):
    username = StringField('Enter your username', validators=[InputRequired("A user message is required"),
                                                              Length(min=4, max=8,
                                                                     message='Must be between 4 and 8 characters')])
    password = PasswordField('Enter your password', validators=[InputRequired("A password is required"),
                                                                AnyOf(values=['secret', 'password'])])
    age = IntegerField('Age', default=24)
    true = BooleanField('Click here if agree')
    email = StringField('Enter your email', validators=[Email()])
    home_phone_number = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    years = FieldList(FormField(YearForm))


class NameForm(LoginForm):
    first_name = StringField('Name')
    last_name = StringField('Last name')


class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email


@app.route('/', methods=['GET', 'POST'])
def index():
    my_user = User('Abel', 28, 'a_v@mail.ru')

    group = namedtuple('Group', ['year', 'total'])
    g1 = group(2005, 1000)
    g2 = group(2021, 200000)
    g3 = group(2023, 400000)

    years = {'years': [g1, g2, g3]}

    form = NameForm(obj=my_user, data=years)

    del form.mobile_phone
    if form.validate_on_submit():
        # return "<h1>Country Code: {} \nArea Code: {}\nNumber: {}</h1>"\
        #     .format(form.home_phone_number.country_code.data,
        #             form.home_phone_number.area_code.data,
        #             form.home_phone_number.number.data)
        # return "<h1>Username {} \nPassword: {}\nAge: {}\nTrue</h1>: {}".format(form.username.data, form.password.data,
        #                                                                        form.age.data, form.true.data)
        output = '<h1>'
        for f in form.years:
            output += 'Year: {}'.format(f.year.data)
            output += 'Total: {}<br>'.format(f.total.data)
        output += '</h1>'

        return output
    return render_template('index.html', form=form)


@app.route('/dynamic', methods=['GET', "POST"])
def dynamic():
    class DynamicForm(FlaskForm):
        pass

    DynamicForm.name = StringField('Name')

    names = ['middle_name', 'last_name', 'nickname', 'main_name']

    for name in names:
        setattr(DynamicForm, name, StringField(name.title()))
    form = DynamicForm()
    if form.validate_on_submit():
        return "<h1>Form has been validated. Name: {}</h1>".format(form.name.data)
    return render_template('dynamic.html', form=form, names=names)


if __name__ == '__main__':
    app.run(debug=True)
