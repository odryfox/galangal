from infrastructure.web import create_app

app = create_app().flask_app

if __name__ == "__main__":
    app.run()
