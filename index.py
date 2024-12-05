from app import create_app

app = create_app()

if __name__ == '__main__':
    app.secret_key = 'es_mi_clave_secreta_12@'
    app.run(debug=True, host="0.0.0.0")
