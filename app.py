from flask import Flask, render_template
from config import Config
from models import init_app
from routes import main, produtos, fornecedores, estoque

app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

app.register_blueprint(main)
app.register_blueprint(produtos, url_prefix='/produtos')
app.register_blueprint(fornecedores, url_prefix='/fornecedores')
app.register_blueprint(estoque, url_prefix='/estoque')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)