from flask import render_template, request, redirect, url_for
from . import fornecedores
from models import mysql

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
        return redirect(url_for('index'))
    return render_template('fornecedores/adicionar.html')