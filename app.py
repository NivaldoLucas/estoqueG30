from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '4512'
app.config['MYSQL_DB'] = 'storage'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        detalhes = request.form
        product_name = detalhes['product_name']
        brand = detalhes['brand']
        quantity = detalhes['quantity']
        price = detalhes['price']
        supplier_id = detalhes['supplier_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products(product_name, brand, quantity, price, supplier_id) VALUES (%s, %s, %s, %s, %s)", (product_name, brand, quantity, price, supplier_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('produtos'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, supplier FROM suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return render_template('adicionar_produto.html', suppliers=suppliers)

@app.route('/adicionar_fornecedor', methods=['GET', 'POST'])
def adicionar_fornecedor():
    if request.method == 'POST':
        detalhes = request.form
        supplier = detalhes['supplier']
        contact = detalhes['contact']
        email = detalhes['email']
        address = detalhes['address']
        site = detalhes['site']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO suppliers(supplier, contact, email, address, site) VALUES (%s, %s, %s, %s, %s)", (supplier, contact, email, address, site))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('adicionar_fornecedor.html')

@app.route('/produtos')
def produtos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.product_name, p.brand, p.quantity, p.price, s.supplier, p.supplier_id FROM products p JOIN suppliers s ON p.supplier_id = s.id")
    products = cur.fetchall()
    cur.close()
    return render_template('produtos.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
