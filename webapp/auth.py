from flask import Blueprint,render_template,flash,redirect,url_for
from .forms import SignUpForm,LoginForm,PasswordChangedForm
from .models import Customer
from . import db
from flask_login import  login_user, login_required, logout_user, current_user,LoginManager,login_manager
from werkzeug.security import generate_password_hash

auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:  # If the user is already logged in, redirect them to the main home
        return redirect(url_for('/'))
    
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        
        customer=Customer.query.filter_by(email=email).first()
        
        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                flash("Login successful!", "success")
                return redirect('/')
            
        flash("Invalid login credentials", "danger")
        
    return render_template('login.html',form=form)
@auth.route('/')
def home():
    return render_template('home.html')

#fff
@auth.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:  # If the user is already logged in, redirect them to the main home
        return redirect(url_for('/'))
    form=SignUpForm()
    if form.validate_on_submit():
        email=form.email.data
        username=form.username.data
        password=form.password.data
        conform_password=form.conform_password.data
        
        if(password == conform_password):
            new_customer=Customer()
            new_customer.email=email
            new_customer.username=username
            new_customer.password=conform_password
            
            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account created successfully Try Login')
                return redirect(url_for('auth.login')) 
            
            except Exception as e :
                print("Error: ",e)  
                flash("Account not created/ Email already exists")
                form.email.data=""
                form.username.data=""
                form.password.data=""
                form.conform_password.data=""
    return render_template('signup.html',form=form)
    
@auth.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth.route('/profile/<int:customer_id>')#profile
@login_required
def profile(customer_id):
    customer=Customer.query.get(customer_id);
    return render_template('profile.html',customer=customer)

# @auth.route('/change_password/<int:customer_id>', methods=['GET','POST'])
# @login_required
# def change_password(customer_id):
#     if current_user.id != customer_id:
#         flash("You cannot change someone else's password", "danger")
#         return redirect(url_for('auth.profile', customer_id=current_user.id))

#     form=PasswordChangedForm()
#     customer=Customer.query.get(customer_id)
#     if form.validate_on_submit():
#         current_password=form.current_password.data
#         new_password=form.new_password.data
#         confirm_new_password=form.confirm_new_password.data
        
         
#         if customer.verify_password(current_password):
#             if(new_password == confirm_new_password):  
#                 customer.password=confirm_new_password 
#                 customer.password = generate_password_hash(confirm_new_password) 
#                 db.session.commit()
#                 flash("password Has been Updated",'success')
#                 return redirect(url_for('auth.profile', customer_id=customer.id))
#             else:
#                 flash("New password do not Match",'danger')
#         else:
#             flash("Incorrect Password",'danger') 
#     return render_template('change_password.html',customer=customer)



@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = PasswordChangedForm()
    customer = Customer.query.get(customer_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Password Updated Successfully')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('New Passwords do not match!!')

        else:
            flash('Current Password is Incorrect')

    return render_template('change_password.html', form=form)