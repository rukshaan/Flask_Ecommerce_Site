from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,FloatField,PasswordField,EmailField,BooleanField,SubmitField
from wtforms .validators import DataRequired,length,NumberRange
from flask_wtf.file import FileField,FileRequired

class SignUpForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired()])
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),length(min=6)])
    conform_password=PasswordField('Conform_Password',validators=[DataRequired(),length(min=6)])
    submit=SubmitField('Sign Up')
    
    
class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),length(min=6)])
    submit=SubmitField('Login')
    
class  PasswordChangedForm(FlaskForm):
    current_password=PasswordField("Current Password",validators=[DataRequired(),length(min=6)])
    new_password=PasswordField("New Password",validators=[DataRequired(),length(min=6)])
    confirm_new_password=PasswordField("Conform password",validators=[DataRequired(),length(min=6)])
    change_password=SubmitField('Change Password')
    
    
class ShopItemForms(FlaskForm):
    product_name=StringField("Product Name :",validators=[DataRequired()]);
    current_price=FloatField("Current Price: ",validators=[DataRequired()])
    previous_price=FloatField("Previous Price: ",validators=[DataRequired()])
    in_stock=IntegerField("Current Stock Count: ",validators=[DataRequired(),NumberRange(min=0)])
    product_picture=FileField("Product Picture",validators=[FileRequired()])
    flash_sale=BooleanField('Flash Sale')
    add_product=SubmitField('Add Product')
    update_product=SubmitField('Update Product')