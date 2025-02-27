from flask import Blueprint,render_template,flash,send_from_directory,redirect
from flask_login import login_required,current_user
from .forms import ShopItemForms,OrderForms
from werkzeug.utils import secure_filename
from .models import Product,Order,Customer
from . import db

admin=Blueprint('admin',__name__)
@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media',filename)


@admin.route('/add_shop_items',methods=['GET','POST'])
@login_required
def add_shop_items():
    if current_user.id==3:
        form=ShopItemForms()
        if form.validate_on_submit():
            product_name=form.product_name.data
            current_price=form.current_price.data
            previous_price=form.previous_price.data
            in_stock=form.in_stock.data
            # product_picture=form.product_picture.data
            flash_sale=form.flash_sale.data
            
            file=form.product_picture.data
            file_name=secure_filename(file.filename)
            file_path=f"./media/{file_name}"
            
            file.save(file_path)
            new_shop_item=Product()
            new_shop_item.product_name=product_name
            new_shop_item.current_price=current_price
            new_shop_item.previous_price=previous_price
            new_shop_item.in_stock=in_stock
            new_shop_item.flash_sale=flash_sale
            new_shop_item.product_picture=file_path
            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added Successfully','success')
                print("Product Added")
                return render_template('add_shop_items.html',form=form)
            except Exception as e:
                print(e)
                print("Data not added successfully")

        return render_template('add_shop_items.html',form=form)
    
    return render_template('404.html')
    
@admin.route('/shop_items',methods=['GET','POST'])
@login_required
def shop_items():
    if(current_user.id ==3):
        items=Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html',items=items)
    return render_template('404.html')
    
    
@admin.route('/update_items/<int:item_id>',methods=['GET','POST'])
@login_required
def update_item(item_id):
    if(current_user.id==3):
        form=ShopItemForms()
        item_to_update=Product.query.get(item_id)
        form.product_name.render_kw={'placeholder':item_to_update.product_name}
        form.previous_price.render_kw={'placeholder':item_to_update.previous_price}
        form.current_price.render_kw={'placeholder':item_to_update.current_price}
        form.in_stock.render_kw={'placeholder':item_to_update.in_stock}
        form.flash_sale.render_kw={'placeholder':item_to_update.flash_sale}
        
        if form.validate_on_submit():
            product_name=form.product_name.data
            previous_price=form.previous_price.data
            current_price=form.current_price.data
            in_stock=form.in_stock.data
            flash_sale=form.flash_sale.data
            file=form.product_picture.data
            file_name=secure_filename(file.filename)
            file_path=f"./media/{file_name}"
            
            file.save(file_path)
            try:
                Product.query.filter_by(id=item_id).update(dict(
                    product_name=product_name,
                    current_price=current_price,
                    previous_price=previous_price,
                    in_stock=in_stock,flash_sale=flash_sale,product_picture=file_path
                ))
                
                db.session.commit()
                flash(f'{product_name} Updated Successfully','success')
                print("Product Updated")
                return redirect('/shop_items')
            except Exception as e:
                print(e)
                print("Data not Updated")
                flash("Data not Updated",'danger')
        return render_template('update_item.html',form=form)
    return render_template('404.html')

@admin.route('/delete_items/<int:item_id>',methods=['GET','POST'])
@login_required
def delete_item(item_id):
    
    if current_user.id ==3:
        try:
            item_to_delete=Product.query.get(item_id)
            print('delete item',item_to_delete.id)
            if not item_to_delete:  # If item is not found
                flash('Item not found', 'danger')
                return redirect('/shop_items')
            
            db.session.delete(item_to_delete)
            db.session.commit()
            # db.session.rollback()

            flash('One item Deleted ','success')
            return redirect('/shop_items')
        except Exception as e:
            print(e)
            print("Data not Deleted")
            flash('Data not Deleted','danger')
        return redirect('/shop_items')
    return render_template('404.html')



@admin.route('/view_orders')
@login_required
def order():
    if current_user.id ==3:
        orders=Order.query.all()
        return render_template('view_orders.html',orders=orders)
    return render_template('404.html')

@admin.route('/update_orders/<int:order_id>',methods=['Get','POST'])
@login_required
def update_Orders(order_id):
    if current_user.id ==3:
        form=OrderForms()
        order=Order.query.get(order_id)
        if form.validate_on_submit():
            status=form.order_status.data
            order.status=status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated Successfully','success')
                return redirect('/view_orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id}not Updated ','danger')
                
            
        return render_template('order_update.html',form=form)
    return render_template('404.html')


@admin.route('/customers',methods=['Get','POST'])
@login_required
def customers():
    if current_user.id==3:
        customers=Customer.query.all()
        return render_template('customers.html',customers=customers)
    return render_template('404.html')

@admin.route('/admin_page',methods=['Get','POST'])
@login_required
def amin_page():
    if current_user.id==3:
        customers=Customer.query.all()
        return render_template('admin.html')
    return render_template('404.html')


# @admin.route('/delete_customers/<int:customer_id>', methods=['POST'])
# @login_required
# def delete_customer(customer_id):
#     # Ensure only admins can delete customers
#     if not current_user.has_role('admin'):
#         flash('Unauthorized access', 'danger')
#         return render_template('404.html')

#     try:
#         customer_to_delete = Customer.query.get(customer_id)
#         if not customer_to_delete:
#             flash('Customer not found', 'danger')
#             return redirect(url_for('customers'))

#         print(f"Deleting customer {customer_to_delete.id}")

#         # Delete customer
#         db.session.delete(customer_to_delete)
#         db.session.commit()

#         flash('One customer Deleted', 'success')
#         return redirect(url_for('customers'))
#     except Exception as e:
#         db.session.rollback()
#         import traceback
#         print("Error deleting customer:", traceback.format_exc())
#         flash('Data not Deleted', 'danger')

#     return redirect(url_for('customers'))