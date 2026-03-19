from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 用户角色关联表
user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),  # 引用 user.user_id
                      db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'), primary_key=True)   # 引用 role.role_id
                      )

# 角色权限关联表
role_permissions = db.Table('role_permissions',
                            db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permission.permission_id'), primary_key=True)
                            )

# 电影类型关联表
movie_genres = db.Table('movie_genres',
                        db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True),  # 引用 movie.movie_id
                        db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)   # 引用 genre.genre_id
                        )

# 用户收藏关联表
user_favorites = db.Table('user_favorites',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
                          db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True),
                          db.Column('created_at', db.DateTime, default=datetime.utcnow)
                          )


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)  # 原 id → user_id
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    region = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    favorites = db.relationship('Movie', secondary=user_favorites, backref=db.backref('favorited_by', lazy='dynamic'))


class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)  # 原 id → role_id
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))


class Permission(db.Model):
    __tablename__ = 'permission'
    permission_id = db.Column(db.Integer, primary_key=True)  # 原 id → permission_id
    name = db.Column(db.String(50), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True)


class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True)  # 原 id → movie_id
    title = db.Column(db.String(200), nullable=False)
    original_title = db.Column(db.String(200))
    description = db.Column(db.Text)
    release_date = db.Column(db.Date)
    duration = db.Column(db.Integer)
    language = db.Column(db.String(50))
    country = db.Column(db.String(100))
    poster_url = db.Column(db.String(500))
    rating = db.Column(db.Float)
    is_blocked = db.Column(db.Boolean, default=False)
    is_sticky = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    genres = db.relationship('Genre', secondary=movie_genres, backref=db.backref('movies', lazy='dynamic'))
    celebrities = db.relationship('MovieCelebrity', back_populates='movie', cascade='all, delete-orphan')
    boxoffices = db.relationship('BoxOffice', back_populates='movie', cascade='all, delete-orphan')


class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True)  # 原 id → genre_id
    name = db.Column(db.String(50), unique=True, nullable=False)


class Celebrity(db.Model):
    __tablename__ = 'celebrity'
    celebrity_id = db.Column(db.Integer, primary_key=True)  # 原 id → celebrity_id
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(100))
    biography = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    is_blocked = db.Column(db.Boolean, default=False)
    is_sticky = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    movies = db.relationship('MovieCelebrity', back_populates='celebrity', cascade='all, delete-orphan')


class MovieCelebrity(db.Model):
    __tablename__ = 'movie_celebrity'
    movie_celebrity_id = db.Column(db.Integer, primary_key=True)  # 原 id → 新增唯一主键
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    celebrity_id = db.Column(db.Integer, db.ForeignKey('celebrity.celebrity_id'), nullable=False)
    role = db.Column(db.String(50))
    character = db.Column(db.String(100))

    movie = db.relationship('Movie', back_populates='celebrities')
    celebrity = db.relationship('Celebrity', back_populates='movies')


class BoxOffice(db.Model):
    __tablename__ = 'box_office'
    boxoffice_id = db.Column(db.Integer, primary_key=True)  # 原 id → boxoffice_id
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float)
    region = db.Column(db.String(50))

    movie = db.relationship('Movie', back_populates='boxoffices')


class UserBehavior(db.Model):
    __tablename__ = 'user_behavior'
    behavior_id = db.Column(db.Integer, primary_key=True)  # 原 id → behavior_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    behavior_type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User')
    movie = db.relationship('Movie')


class RecommendationConfig(db.Model):
    __tablename__ = 'recommendation_config'
    config_id = db.Column(db.Integer, primary_key=True)  # 原 id → config_id
    algorithm = db.Column(db.String(50))
    weight = db.Column(db.Float)
    enabled = db.Column(db.Boolean, default=True)


class RecommendationResult(db.Model):
    __tablename__ = 'recommendation_result'
    result_id = db.Column(db.Integer, primary_key=True)  # 原 id → result_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    score = db.Column(db.Float)
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User')
    movie = db.relationship('Movie')


class ManualIntervention(db.Model):
    __tablename__ = 'manual_intervention'
    intervention_id = db.Column(db.Integer, primary_key=True)  # 原 id → intervention_id
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'))
    action = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime)

    movie = db.relationship('Movie')


class SystemLog(db.Model):
    __tablename__ = 'system_log'
    log_id = db.Column(db.Integer, primary_key=True)  # 原 id → log_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    action = db.Column(db.String(200))
    ip = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User')


class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    config_id = db.Column(db.Integer, primary_key=True)  # 原 id → config_id
    key = db.Column(db.String(100), unique=True)
    value = db.Column(db.Text)
    description = db.Column(db.String(200))