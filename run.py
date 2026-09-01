from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True recargará el servidor automáticamente cuando guardes cambios
    app.run(debug=True)