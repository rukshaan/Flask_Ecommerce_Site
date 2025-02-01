from flask import Blueprint,render_template,flash,redirect,request,jsonify
from flask_login import login_required,current_user
from .models import Product,Cart,Order
from . import db
from intasend import APIService
views=Blueprint('views',__name__)

API_PUBLISHABLE_KEY='ISPubKey_test_4aaa7726-4542-4c38-a284-70afe13103fd'

API_TOKEN='ISSecretKey_test_da9dd0d3-ecfd-4d1f-8b9e-7cbadf6c3f7b'

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
    
    

API_PUBLISHABLE_KEY='ISPubKey_test_4aaa7726-4542-4c38-a284-70afe13103fd'

API_TOKEN='ISSecretKey_test_da9dd0d3-ecfd-4d1f-8b9e-7cbadf6c3f7b'


@views.route('/place-order')   
@login_required
def place_order():
    customer_cart=Cart.query.filter_by(customer_link=current_user.id)
    if customer_cart:
        
            total=0
            total=sum(item.product.current_price *item.quantity for item in customer_cart)
            service=APIService(token=API_TOKEN,test=True)    
            try:
                create_order_response = service.collect.mpesa_stk_push(
                    phone_number='0778901558',
                    email='shaanruk0309@gmail.com',
                    amount=100,
                    narrative='Purchase of goods'
                )

                print("Response:",create_order_response)
                # if create_order_response.get('status') != 'success':
                #     flash('Payment failed, please try again.', 'danger')
                #     return redirect("/")
        
            

                for item in customer_cart:
                    new_order=Order()
                    new_order.quantity=item.quantity
                    new_order.price=item.product.current_price
                    new_order.status=create_order_response['invoice']['state'].capitalize()
                    new_order.payment_id=create_order_response['id']
                    new_order.customer_link = current_user.id  #  Assign the logged-in user's ID
                    new_order.product_link = item.product_link  #  Ensure correct linkage
                    db.session.add(new_order)
                    
                    product=Product.query.get(item.product_link)
                    if product:
                        product.in_stock-=item.quantity
                    db.session.delete(item)
                db.session.commit()
                flash("order is placed",'success')
                return redirect('orders')
            
            except Exception as e:
                print(e)
                print("order is not placed")
                flash('order is not placed','danger')
                return redirect("/")
    else :
        flash('Your card is empty !!!','danger')


@views.route('/orders')
@login_required
def order():
    order=Order.query.filter_by(customer_link = current_user.id).all()
    return render_template('orders.html',orders=order)

# @views.route('/search')
# def search():
#     if request.method =='POST':
#         search_query=request.form.get('search')
#         items=Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        
#         return render_template('search.html',items=items,cart=Cart.query.filter_by(customer_link=current_user.id).all()
#                            if current_user.is_authenticated else [])
#     return render_template("search.html")



@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST': 
        search_query = request.form.get('search')

        if search_query:  
            items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
            return render_template(
                'search.html',
                items=items,
                cart=Cart.query.filter_by(customer_link=current_user.id).all()
                if current_user.is_authenticated else []
            )
        else:
            flash("Please enter a search query.", "warning")
            return redirect('/search')
    return render_template("search.html", items=[] if request.method == 'GET' else None)
