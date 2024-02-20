from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)


class Product (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<Product id:%r, name:%r, description:%r, price:%r, available:%r>' % (self.id, self.name, self.description, self.price, self.is_available)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    products = Product.query.order_by(Product.price).all()
    return render_template('index.html', products=products)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        is_available = request.form['is_available'] == 'on'
        product = Product(name=name, description=description, price=price, is_available=is_available)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении товара произошла ошибка'
    else:
        return render_template('add-product.html')


if __name__ == '__main__':
    app.run(debug=True)