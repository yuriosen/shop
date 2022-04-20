from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, logout_user
from data.db_session import global_init, create_session
from forms.user import RegisterForm, LoginForm
from forms.add_job import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/job',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.name.data
        job.product = form.product.data
        job.price = form.price.data
        job.description = form.description.data
        job.bargaining = form.bargaining.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Adding a job',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            phone_number=form.phone_number.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


def create_products():
    db_sess = db_session.create_session()
    capitane = User()
    capitane.surname = 'Scott'
    capitane.name = 'Ridley'
    capitane.age = 21
    capitane.position = 'capitane'
    capitane.speciality = 'research engineer'
    capitane.address = 'module_1'
    capitane.email = 'scott_chief@mars.org'

    pilot = User()
    pilot.surname = 'Weir'
    pilot.name = 'Andy'
    pilot.age = 25
    pilot.position = 'pilot'
    pilot.speciality = 'pilot'
    pilot.address = 'module_2'
    pilot.email = 'weir@mars.org'

    builder = User()
    builder.surname = 'Watney'
    builder.name = 'Mark'
    builder.age = 22
    builder.position = 'builder'
    builder.speciality = 'builder'
    builder.address = 'module_3'
    builder.email = 'watney@mars.org'

    biolog = User()
    biolog.surname = 'Sanders'
    biolog.name = 'Taddy'
    biolog.age = 18
    biolog.position = 'biolog'
    biolog.speciality = 'biolog'
    biolog.address = 'module_4'
    biolog.email = 'sanders@mars.org'

    db_sess = db_session.create_session()
    db_sess.add(capitane)
    db_sess.add(pilot)
    db_sess.add(builder)
    db_sess.add(biolog)
    db_sess.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Wrong login and password",
                               form=form)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    name = 'base'
    global_init(name)
    db_sess = create_session()

    app.run()


if __name__ == '__main__':
    main()