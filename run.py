from app import create_app


def run():
    app = create_app()
    app.run(debug=True, host="0.0.0.0")

if __name__ == '__main__':
    run()
