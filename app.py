from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

CSV_FILE = 'products.csv'


# Dashboard route
@app.route('/')
def dashboard():
    products = []
    low_stock = 0
    healthy_stock = 0

    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            quantity = int(row['quantity'])
            threshold = int(row['threshold'])

            status = "Low" if quantity <= threshold else "Healthy"

            if status == "Low":
                low_stock += 1
            else:
                healthy_stock += 1

            products.append({
                'name': row['name'],
                'quantity': quantity,
                'status': status
            })

    total_products = len(products)

    return render_template(
        'dashboard.html',
        products=products,
        total=total_products,
        low=low_stock,
        healthy=healthy_stock
    )


# Add product page
@app.route('/add')
def add_product():
    return render_template('add_product.html')


# Handle form submit
@app.route('/add-product', methods=['POST'])
def add_product_post():
    name = request.form['name']
    quantity = request.form['quantity']
    threshold = request.form['threshold']

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['name', 'quantity', 'threshold'])
        writer.writerow([name, quantity, threshold])

    return redirect('/')
    
@app.route('/delete/<name>')
def delete_product(name):
    rows = []

    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] != name:
                rows.append(row)

    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'quantity', 'threshold'])
        writer.writeheader()
        writer.writerows(rows)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
