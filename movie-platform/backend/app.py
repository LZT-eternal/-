from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from auth import auth_bp
from api.movies import movies_bp
from api.celebrities import celebrities_bp
from api.boxoffice import boxoffice_bp
from api.recommendations import recommendations_bp
from api.users import users_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    CORS(app, resources={r"/api/*": {"origins": "*"}, r"/auth/*": {"origins": "*"}})
    db.init_app(app)
    jwt = JWTManager(app)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(celebrities_bp)
    app.register_blueprint(boxoffice_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(users_bp)

    # 创建数据库表（开发环境使用）
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)