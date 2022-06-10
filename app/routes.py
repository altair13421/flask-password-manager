from flask import Flask, redirect, render_template, request, url_for, flash
from app import db, app
from .forms import LoginForm, EntryForm, SignupForm
from .models import Users, Passwords
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
import pyperclip as ppc

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User': Users, 'Passwords': Passwords}

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html', 
        title="Home", 
        homething="Password Manager",
        homelink=url_for('index'),
        heading="Home", 
        hrefdata = url_for('login'), 
        entry_1="Signup", 
        entry_1_link = url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = SignupForm()
    if form.validate_on_submit():
        if Users.query.filter_by(username=form.username.data).first() != None:
            flash('User Exists, Please Login')
            return redirect('login')
        user = Users(username=f'{form.username.data}')
        user.set_password(f'{form.password.data}')
        db.session.add(user)
        db.session.commit()
        flash(f'User {form.username.data} Registered')
        return redirect('login')
    return render_template(
        'signup.html', 
        title="Sign Up - Password Manager", 
        homething="Password Manager",
        homelink=url_for('index'),
        form = form, 
        entry_1="Signup", 
        entry_1_link = url_for('signup'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)
    return render_template(
        'login.html', 
        title="Login - Password Manager", 
        homething="Password Manager",
        homelink=url_for('index'),
        form = form,  
        entry_1="Signup", 
        entry_1_link = url_for('signup'))

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    allitems = Passwords.query.filter_by(userid=current_user.id)
    return render_template(
        'mainpage.html', 
        title="Passwords - Password Manager", 
        homething=f"Welcome {current_user.username}",
        homelink=url_for('index'),
        entry_1="Add", 
        entry_1_link = url_for('add_entry'), 
        allitems=allitems)

@app.route('/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    form = EntryForm()
    id = None
    # if request.args:
    #     username = request.args.get('username')
    #     password = request.args.get('password')
    #     url = request.args.get('url')
    #     name = request.args.get('name')
    #     description = request.args.get('description')
    #     id = request.args.get('id')

    if form.validate_on_submit():
        tosave = Passwords(
            username = form.username.data,
            password = form.password.data,
            name = form.name.data,
            url = form.url.data,
            description = form.description.data,
            userid = current_user.id
        )
        db.session.add(tosave)
        db.session.commit()
        flash('Entry Saved')
        return redirect(url_for('main'))
    return render_template(
        'addentry.html', 
        title="Add Entry - Password Manager", 
        homething="<",
        homelink=url_for('main'),
        form = form, 
        entry_1="Discard", 
        entry_1_link = url_for('main'), 
    )

@app.route('/view/<id>', methods=['GET', 'POST'])
@login_required
def view(id):
    data = Passwords.query.get(id)
    return render_template(
        'viewpage.html', 
        title=f"{data.name} - Password Manager", 
        homething="<",
        homelink=url_for('main'),
        entry_1="Edit", 
        entry_1_link = url_for('edit', id=id), 
        data = data)

@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
        flash('For Editing. Delete First, and Re add')
        return redirect(url_for('main'))


@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id, edit = False):
    data = Passwords.query.get(id)
    db.session.delete(data)
    db.session.commit()
    if not edit:
        return redirect(url_for('main'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/copy/<data>', methods=['GET', 'POST'])
@login_required
def copydata(data):
    ppc.copy(data)
    return redirect(url_for('view', id=request.args.get('id')))