from flask import render_template, request, redirect, url_for
from . import estoque
from models import mysql

@estoque.route('/')
def listar_estoque():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name, brand, quantity, price, supplier FROM storage")
    estoque = cur.fetchall()
    cur.close()
    return render_template('estoque/listar.html', estoque=estoque)

@estoque.route('/adicionar', methods=['GET', 'POST'])
def adicionar_estoque():
    if request.method == 'POST':
        detalhes = request.form
        product_id = detalhes['product_id']
        quantity = detalhes['quantity']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT p.product_name, p.brand, p.price, s.supplier FROM products p JOIN suppliers s ON p.supplier_id = s.id WHERE p.id = %s", [product_id])
        product = cur.fetchone()
        
        cur.execute("INSERT INTO storage(product_name, brand, quantity, price, supplier) VALUES (%s, %s, %s, %s, %s)", (product[0], product[1], quantity, product[2], product[3]))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('estoque.listar_estoque'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('estoque/adicionar.html', products=products)

@estoque.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_estoque(id):
    if request.method == 'POST':
        detalhes = request.form
        quantity = detalhes['quantity']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE storage 
            SET quantity = %s
            WHERE id = %s
        """, (quantity, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('estoque.listar_estoque'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, brand, quantity, price, supplier FROM storage WHERE id = %s", [id])
    product = cur.fetchone()
    cur.close()
    return render_template('estoque/editar.html', product=product)