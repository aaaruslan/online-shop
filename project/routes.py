from project import app, db, bcrypt
from project.forms import RegistrationForm, LogInForm, UpdateAccountForm, AddProductForm, DeleteProductForm
from project.models import User, Product
from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/reg', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data)
        email = form.email.data
        db.session.add(User(username=username, password=password, email=email))
        db.session.commit()
        return redirect(url_for('log_in'))
    return render_template('registration.html', form=form)

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LogInForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalars().first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main_page'))
    return render_template('log_in.html', form=form)

@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('main_page'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form, with_navbar=True)

@app.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    products = db.paginate(db.select(Product), per_page=3, page=page)
    return render_template('catalog.html', products=products, with_navbar=True)

@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.username == 'admin':
        form = AddProductForm()
        if form.validate_on_submit():
            product = Product(title=form.title.data, description=form.description.data, price=form.price.data)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('add_product'))
        return render_template('add_product.html', form=form, with_navbar=True)
    else:
        return redirect(url_for('main_page'))

@app.route('/catalog/delete', methods=['GET', 'POST'])
@login_required
def delete_product():
    if current_user.username == 'admin':
        form = DeleteProductForm()
        if form.validate_on_submit():
            title = form.title_to_delete.data
            product_to_delete = db.session.execute(db.select(Product).where(Product.title == title)).scalars().first()
            db.session.delete(product_to_delete)
            db.session.commit()
            return redirect(url_for('delete_product'))
        return render_template('delete_product.html', form=form, with_navbar=True)
    else:
        return redirect(url_for('main_page'))


@app.route('/')
def main_page():
    return render_template('main_page.html', with_navbar=True)