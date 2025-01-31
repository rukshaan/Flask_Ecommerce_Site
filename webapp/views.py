from flask import Blueprint,render_template,flash,redirect,request,jsonify
from flask_login import login_required,current_user
from .models import Product,Cart
from . import db
views=Blueprint('views',__name__)

@views.route('/')
def home():
    items=Product.query.filter_by(flash_sale=True)
    return render_template('home.html',items=items,cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route('/add_to_card/<int:item_id>',methods=['GET','POST'])
@login_required
def add_to_card(item_id):
    item_to_add=Product.query.get(item_id)
    if not item_to_add:
        flash('Item not found', 'danger')
        return redirect(request.referrer)  # Redirect to the previous page if item doesn't exist

    item_exists=Cart.query.filter_by(product_link=item_id,customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity=item_exists.quantity+1
            db.session.commit()
            flash(f' {item_exists.product.product_name} has been Updated ','success')
            return redirect(request.referrer)
        except Exception as e:
            db.session.rollback()
            print("Quantity not udated",e)
            flash(f'{item_exists.product.product_name} not Updated ','error')
            return redirect(request.referrer)
            
    new_card_item=Cart()
    new_card_item.quantity=1
    new_card_item.product_link=item_to_add.id
    new_card_item.customer_link=current_user.id
         
    try:
        db.session.add(new_card_item)
        db.session.commit()
        flash(f'{new_card_item.product.product_name} added to card..')
        
    except Exception as e:
        db.session.rollback()
        flash(f'{new_card_item.product.product_name} has not been added to card..')
        
    return redirect(request.referrer)  # Redirect to the previous page

@views.route('/cart')
@login_required
def show_cart():
    cart=Cart.query.filter_by(customer_link=current_user.id).all()
    amount=0
    for item in cart:
        amount+=item.product.current_price * item.quantity
        
    return render_template('cart.html',cart=cart,amount=amount,total=amount+200)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method =='GET':
        cart_id=request.args.get('cart_id')
        cart_item=Cart.query.get(cart_id)
        cart_item.quantity=cart_item.quantity+1
        db.session.commit()
        
        cart=Cart.query.filter_by(customer_link=current_user.id).all()
        amount=0
        for item in cart:
            amount+=item.product.current_price *item.quantity
        data={
            'Response':'Backend Response',
            'quantity':cart_item.quantity,
            'amount':amount,
            'total':amount+200
        }
        return jsonify(data)
    
    
@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method =='GET':
        cart_id=request.args.get('cart_id')
        cart_item=Cart.query.get(cart_id)
        cart_item.quantity=cart_item.quantity-1
        db.session.commit()
        
        cart=Cart.query.filter_by(customer_link=current_user.id).all()
        amount=0
        for item in cart:
            amount+=item.product.current_price *item.quantity
        data={
            'Response':'Backend Response',
            'quantity':cart_item.quantity,
            'amount':amount,
            'total':amount+200
        }
        return jsonify(data)
    
    
    
   
@views.route('/removecart')
@login_required
def remove_cart():
    if request.method =='GET':
        cart_id=request.args.get('cart_id')
        cart_item=Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()
        
        cart=Cart.query.filter_by(customer_link=current_user.id).all()
        amount=0
        for item in cart:
            amount+=item.product.current_price *item.quantity
        data={
            'Response':'Backend Response',
            'quantity':cart_item.quantity,
            'amount':amount,
            'total':amount+200
        }
        return jsonify(data)
    
    