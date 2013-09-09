from flask import Flask, render_template, request, session

import settings
import models

app = Flask(__name__)
app.config.from_object(settings)

__VERSION__ = "0.1"

@app.route("/")
def hello():
    products = models.Product.query.all()
    return render_template('index.html', 
                           products = products)
    
    
@app.route("/product/add", methods=['GET', 'POST'])
def product_add():
    if request.method == "GET":
        return render_template("create_product.html")
    if request.method == "POST":
        name = request.form['name'] 
        description = request.form['description']
        product = models.Product(name, description)
        session.add(product)
        sessions.save()
     


if __name__ == "__main__":
    app.run()
