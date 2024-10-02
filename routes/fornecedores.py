from flask import render_template, request, redirect, url_for
from . import fornecedores
from models import mysql

@fornecedores.route('/')
def listar_fornecedores():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, supplier, contact, email, address, site FROM suppliers")
    fornecedores = cur.fetchall()
    cur.close()
    return render_template('fornecedores/listar.html', fornecedores=fornecedores)

@fornecedores.route('/adicionar', methods=['GET', 'POST'])
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
        return redirect(url_for('fornecedores.listar_fornecedores'))
    
    return render_template('fornecedores/adicionar.html')

@fornecedores.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    if request.method == 'POST':
        detalhes = request.form
        supplier = detalhes['supplier']
        contact = detalhes['contact']
        email = detalhes['email']
        address = detalhes['address']
        site = detalhes['site']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE suppliers 
            SET supplier = %s, contact = %s, email = %s, address = %s, site = %s 
            WHERE id = %s
        """, (supplier, contact, email, address, site, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('fornecedores.listar_fornecedores'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT supplier, contact, email, address, site FROM suppliers WHERE id = %s", [id])
    fornecedor = cur.fetchone()
    cur.close()
    return render_template('fornecedores/editar.html', fornecedor=fornecedor)

@fornecedores.route('/deletar/<int:id>', methods=['GET', 'POST'])
def deletar_fornecedor(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM suppliers WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('fornecedores.listar_fornecedores'))