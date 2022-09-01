from flask import Flask


    

def create_app():
    
    app = Flask(__name__)

    from flask_app.routes.main_bp import main_bp
    

    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
    
