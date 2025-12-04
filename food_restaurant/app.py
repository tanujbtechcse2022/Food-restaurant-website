from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy user database
users = {}

# Menu items
menu_items = [
    {'id': 1, 'name': 'Paneer Tikka', 'price': 250, 'image': 'pt.jpg'},
    {'id': 2, 'name': 'Vegetable Pakora', 'price': 150, 'image': 'pokora-5526036_1280.jpg'},
    {'id': 3, 'name': 'Samosa', 'price': 20, 'image': 'food-2217013_1280.jpg'},
    {'id': 4, 'name': 'Butter Chicken', 'price': 350, 'image': 'butter-chicken-7614835_1280.jpg'},
    {'id': 5, 'name': 'Dal Makhani', 'price': 200, 'image': 'jdls.jpg'},
    {'id': 6, 'name': 'Palak Paneer', 'price': 280, 'image': 'palak.webp'},
    {'id': 7, 'name': 'Chicken Biryani', 'price': 350, 'image': 'cick.webp'},
    {'id': 8, 'name': 'Veg Biryani', 'price': 250, 'image': 'veg biryani.webp'},
    {'id': 9, 'name': 'Gulab Jamun', 'price': 40, 'image': 'gb.jpg'},
    {'id': 10, 'name': 'Ras Malai', 'price': 120, 'image': 'ras.jpg'}
]

@app.route('/')
def home():
    return render_template('web.html', menu_items=menu_items)

@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    item = next((x for x in menu_items if x['id'] == item_id), None)
    if item:
        cart = session.get('cart', [])
        cart.append(item)
        session['cart'] = cart
    return redirect(url_for('home'))

@app.route('/cart')
def view_cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('home'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['lock']
        if username in users:
            return "Username already exists!"
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['lock']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('cart', None)
    return redirect(url_for('home'))

@app.route('/place_order')
def place_order():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Optionally: You could save the order to a file or database here

    # Clear the cart after ordering
    session.pop('cart', None)

    return render_template('order_success.html')


if __name__ == '__main__':
    app.run(debug=True)
