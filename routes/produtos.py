from flask import render_template, request, redirect, url_for
from . import produtos
from models import mysql

@produtos.route('/produtos')
def listar_produtos():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, p.product_name, p.brand, p.price, s.supplier 
        FROM products p 
        JOIN suppliers s ON p.supplier_id = s.id
    """)
    products = cur.fetchall()
    cur.close()
    return render_template('produtos.html', products=products)

@produtos.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        detalhes = request.form
        product_name = detalhes['product_name']
        brand = detalhes['brand']
        price = detalhes['price']
        supplier_id = detalhes['supplier_id']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products(product_name, brand, price, supplier_id) VALUES (%s, %s, %s, %s)", (product_name, brand, price, supplier_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('produtos.listar_produtos'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, supplier FROM suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return render_template('adicionar_produto.html', suppliers=suppliers)

@produtos.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if request.method == 'POST':
        detalhes = request.form
        product_name = detalhes['product_name']
        brand = detalhes['brand']
        price = detalhes['price']
        supplier_id = detalhes['supplier_id']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE products 
            SET product_name = %s, brand = %s, price = %s, supplier_id = %s 
            WHERE id = %s
        """, (product_name, brand, price, supplier_id, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('produtos.listar_produtos'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, brand, price, supplier_id FROM products WHERE id = %s", [id])
    product = cur.fetchone()
    cur.execute("SELECT id, supplier FROM suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return render_template('editar_produto.html', product=product, suppliers=suppliers)

@produtos.route('/deletar_produto/<int:id>', methods=['GET', 'POST'])
def deletar_produto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('produtos.listar_produtos'))