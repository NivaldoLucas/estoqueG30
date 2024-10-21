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
        price = detalhes['price']
        supplier_id = detalhes['supplier_id']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO products(product_name, brand, price, supplier_id) VALUES (%s, %s, %s, %s)", (product_name, brand, price, supplier_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('produtos'))  # Redireciona para a página de produtos
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, supplier FROM suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return render_template('adicionar_produto.html', suppliers=suppliers)

@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('produtos'))  # Redireciona para a página de produtos
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, brand, price, supplier_id FROM products WHERE id = %s", [id])
    product = cur.fetchone()
    cur.execute("SELECT id, supplier FROM suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return render_template('editar_produto.html', product=product, suppliers=suppliers)

@app.route('/deletar_produto/<int:id>', methods=['GET', 'POST'])
def deletar_produto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('produtos'))  # Redireciona para a página de produtos

@app.route('/adicionar_estoque', methods=['GET', 'POST'])
def adicionar_estoque():
    if request.method == 'POST':
        detalhes = request.form
        product_id = detalhes['product_id']
        quantity = detalhes['quantity']
        
        # Obter detalhes do produto
        cur = mysql.connection.cursor()
        cur.execute("SELECT p.product_name, p.brand, p.price, s.supplier FROM products p JOIN suppliers s ON p.supplier_id = s.id WHERE p.id = %s", [product_id])
        product = cur.fetchone()
        
        # Inserir o produto na tabela storage
        cur.execute("INSERT INTO storage(product_name, brand, quantity, price, supplier) VALUES (%s, %s, %s, %s, %s)", (product[0], product[1], quantity, product[2], product[3]))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('estoque'))  # Redireciona para a página de estoque
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('adicionar_estoque.html', products=products)

@app.route('/editar_estoque/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('estoque'))  # Redireciona para a página de estoque
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_name, brand, quantity, price, supplier FROM storage WHERE id = %s", [id])
    product = cur.fetchone()
    cur.close()
    return render_template('editar_estoque.html', product=product)

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
        return redirect(url_for('fornecedores'))
    return render_template('adicionar_fornecedor.html')

@app.route('/editar_fornecedor/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    if request.method == 'POST':
        detalhes = request.form
        supplier = detalhes['supplier_name']
        contact = detalhes['celphone']
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
        return redirect(url_for('fornecedores'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT supplier, contact, email, address, site FROM suppliers WHERE id = %s", [id])
    suppliers = cur.fetchone()
    cur.close()
    return render_template('editar_fornecedor.html', suppliers=suppliers)

@app.route('/deletar_fornecedor/<int:id>', methods=['GET', 'POST'])
def deletar_fornecedor(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM suppliers WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('fornecedores'))

@app.route('/adicionar_patrimonio', methods=['GET', 'POST'])
def adicionar_patrimonio():
    if request.method == 'POST':
        detalhes = request.form
        nome = detalhes['nome']
        marca = detalhes['marca']
        setor = detalhes['setor']
        quantidade = detalhes['quantidade']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patrimonio(nome, marca, setor, quantidade) VALUES (%s, %s, %s, %s)", (nome, marca, setor, quantidade))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('patrimonio'))
    
    return render_template('adicionar_patrimonio.html')

@app.route('/editar_patrimonio/<int:id>', methods=['GET', 'POST'])
def editar_patrimonio(id):
    if request.method == 'POST':
        detalhes = request.form
        nome = detalhes['nome']
        marca = detalhes['marca']
        setor = detalhes['setor']
        quantidade = detalhes['quantidade']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE patrimonio 
            SET nome = %s, marca = %s, setor = %s, quantidade = %s 
            WHERE id = %s
        """, (nome, marca, setor, quantidade, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('patrimonio'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT nome, marca, setor, quantidade FROM patrimonio WHERE id = %s", [id])
    patrimonio = cur.fetchone()
    cur.close()
    return render_template('editar_patrimonio.html', patrimonio=patrimonio)

@app.route('/deletar_patrimonio/<int:id>', methods=['GET', 'POST'])
def deletar_patrimonio(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM patrimonio WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('patrimonio'))

@app.route('/produtos')
def produtos():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.id, p.product_name, p.brand, p.price, s.supplier 
        FROM products p 
        JOIN suppliers s ON p.supplier_id = s.id
    """)
    products = cur.fetchall()
    cur.close()
    return render_template('produtos.html', products=products)

@app.route('/estoque')
def estoque():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, product_name, brand, quantity, price, supplier FROM storage")
    estoque = cur.fetchall()
    cur.close()
    return render_template('estoque.html', estoque=estoque)

@app.route('/fornecedores')
def fornecedores():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, supplier, contact, email, address, site FROM suppliers")
    fornecedores = cur.fetchall()
    cur.close()
    return render_template('fornecedores.html', fornecedores=fornecedores)

@app.route('/patrimonio')
def patrimonio():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nome, marca, setor, quantidade FROM patrimonio")
    patrimonios = cur.fetchall()
    cur.close()
    return render_template('patrimonio.html', patrimonios=patrimonios)

if __name__ == '__main__':
    app.run(debug=True)