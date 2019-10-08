from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/HotSauce')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.hotsauce
cart = db.cart

# comments = db.comments

app = Flask(__name__)

# items = [
#     { 'title': 'Hot sauce', 'description': 'hottest sauce on the planet', 'price': '100', 'img': 'https://images-na.ssl-images-amazon.com/images/I/71Jsiqz0aiL._SL1500_.jpg', 'item_id': '1'},
#     { 'title': 'Sriratcha', 'description': 'Dont mess with it very hot !', 'price': '100', 'img': 'https://images-na.ssl-images-amazon.com/images/I/41MuzdQojXL._SX425_.jpg', 'item_id': '12'},
#     { 'title': 'Sriratcha', 'description': 'Dont mess with it very hot !', 'price': '100', 'img': 'https://images-na.ssl-images-amazon.com/images/I/41MuzdQojXL._SX425_.jpg', 'item_id': '123'},
#     { 'title': 'Sriratcha', 'description': 'Dont mess with it very hot !', 'price': '100', 'img': 'https://images-na.ssl-images-amazon.com/images/I/41MuzdQojXL._SX425_.jpg', 'item_id': '1234'},
#     { 'title': 'Sriratcha', 'description': 'Dont mess with it very hot !', 'price': '100', 'img': 'https://images-na.ssl-images-amazon.com/images/I/41MuzdQojXL._SX425_.jpg', 'item_id': '12345'},
#     { 'title': 'Sriratcha', 'description': 'Dont mess with it very hot !', 'price': '100', 'img': 'https://images-na.ssl-images-amazon.com/images/I/41MuzdQojXL._SX425_.jpg', 'item_id': '123456'}
# ]

@app.route('/')
def hot_sauce_index():
    """Show all playlists."""
    return render_template('index.html', items=items.find())

@app.route('/hotsauce/shop')
def hot_sauce_show():
    """Show all playlists."""
    return render_template('shop.html', items=items.find())

@app.route('/item/new')
def playlists_new():
    """Create a new item."""
    return render_template('new_item.html', item={}, title='New Item')

@app.route('/items', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'img': request.form.get('images'),
        'created_at': datetime.now()
    }
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('item_display', item_id=item_id))

@app.route('/shop/item/<item_id>', methods=['POST', 'GET'])
@app.route('/hotsauce/shop/item/<item_id>', methods=['POST', 'GET'])
def item_display(item_id):
    """Show a single playlist."""
    item = items.find_one({'_id': ObjectId(item_id)})
    # playlist_comments = comments.find({'item_id': ObjectId(item_id)})
    return render_template('show_single_item.html', items=item)

@app.route('/hotsauce/shop/item/shopping_cart/<item_id>', methods=['POST', 'GET'])
@app.route('/shop/item/shopping_cart/<item_id>', methods=['POST', 'GET'])
def add_shopping_cart(item_id):
    """Show a single playlist."""
    item = items.find_one({'_id': ObjectId(item_id)})
    # item.update = ({'quantity': 1})
    cart.item = item
    cart.save(item)
    cart_items = cart.find()
    return render_template('shopping_cart.html', cart_items=cart_items)

@app.route('/shopping_cart/<item_id>', methods=['POST', 'GET'])
def show_shopping_cart(item_id):
    """Show a single playlist."""
    cart_items = cart.find()
    return render_template('shopping_cart.html', cart_items=cart_items)

@app.route('/items/<item_id>/edit', methods=['POST'])
def items_edit(item_id):
    """Show the edit form for a item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('edit_item.html', item=item, title='Edit Item')
#
@app.route('/item/<item_id>', methods=['POST'])
def items_update(item_id):
    """Submit an edited item."""
    updated_item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'img': request.form.get('images'),
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})
    return redirect(url_for('item_display', item_id=item_id))


@app.route('/items/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    """Delete one item."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('hot_sauce_index'))

@app.route('/cart/<cart_id>/delete', methods=['POST'])
def cart_delete(cart_id):
    """Delete one item."""
    cart.delete_one({'_id': ObjectId(cart_id)})
    return redirect(url_for('show_shopping_cart', item_id=cart_id))


#
# @app.route('/playlists/comments', methods=['POST'])
# def comments_new():
#     """Submit a new comment."""
#     comment = {
#         'title': request.form.get('title'),
#         'content': request.form.get('content'),
#         'playlist_id': ObjectId(request.form.get('playlist_id'))
#     }
#     print(comment)
#     comment_id = comments.insert_one(comment).inserted_id
#     return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))
#
# @app.route('/playlists/comments/<comment_id>', methods=['POST'])
# def comments_delete(comment_id):
#     """Action to delete a comment."""
#     comment = comments.find_one({'_id': ObjectId(comment_id)})
#     comments.delete_one({'_id': ObjectId(comment_id)})
#     return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))




if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
