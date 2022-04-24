from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from data.product import Product
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.product import ProductForm
from data import product_api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/product_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def product_delete(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.id == id,
                                            Product.user == current_user
                                            ).first()
    if product:
        db_sess.delete(product)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        product = db_sess.query(Product).filter(Product.id == id,
                                                Product.user == current_user
                                                ).first()
        if product:
            form.title.data = product.title
            form.content.data = product.content
            form.price.data = product.price
            form.bargaining.data = product.bargaining
            form.photo.data = product.photo
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = db_sess.query(Product).filter(Product.id == id,
                                                Product.user == current_user
                                                ).first()
        if product:
            product.title = form.title.data
            product.content = form.content.data
            product.price = form.price.data
            product.bargaining = form.bargaining.data
            product.photo = form.photo.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('product.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        product = Product()
        product.title = form.title.data
        product.content = form.content.data
        product.price = form.price.data
        product.bargaining = form.bargaining.data
        product.photo = form.photo.data
        current_user.product.append(product)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('product.html', title='Добавление товара',
                           form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        product = db_sess.query(Product).filter(
            (Product.user == current_user) | (Product.is_private != True))
    else:
        product = db_sess.query(Product).filter(Product.is_private != True)
    return render_template("index.html", product=product)


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
            name=form.name.data,
            email=form.email.data,
            number=form.number.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def create_user(name, email, number):
    user = User()
    user.name = name
    user.email = email
    user.number = number
    return user


def create_users():
    user1 = create_user("Пользователь 1", "email@email.ru", "11111")
    user2 = create_user("Пользователь 2", "email2@email.ru", "22222")
    user3 = create_user("Пользователь 3", "email_3@email.ru", "33333")
    db_sess = db_session.create_session()
    db_sess.add(user1)
    db_sess.add(user2)
    db_sess.add(user3)
    db_sess.commit()


def create_product_():
    db_sess = db_session.create_session()
    product = Product(title="Сумка", content="Красивая красная сумка", price="16",
                      user_id=1, is_private=False, bargaining=False, photo='/static/img/bag.jpg')
    db_sess.add(product)

    user = db_sess.query(User).filter(User.id == 1).first()
    product = Product(title="Стол", content="деревянный, большой", price="100",
                      user=user, is_private=False, bargaining=True, photo='/static/img/table.jpg')
    db_sess.add(product)

    user.product.append(product)
    db_sess.commit()


def main():
    db_session.global_init('data/shop.db')
    create_users()
    create_product_()
    app.register_blueprint(product_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
