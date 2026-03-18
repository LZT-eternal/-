from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Movie, UserBehavior, RecommendationResult, RecommendationConfig, ManualIntervention, User
from datetime import datetime
from sqlalchemy import desc
import random

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')


# 为用户获取推荐列表（简单示例：基于热门和协同过滤混合）
@recommendations_bp.route('/user', methods=['GET'])
@jwt_required()
def get_recommendations():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': '用户不存在'}), 404

    # 获取用户最近行为（用于个性化）
    recent_behaviors = UserBehavior.query.filter_by(user_id=user.id).order_by(desc(UserBehavior.created_at)).limit(
        20).all()
    recent_movie_ids = [b.movie_id for b in recent_behaviors if b.movie_id]

    # 简单推荐逻辑：
    # 1. 获取热门电影（全局点击量高的）
    popular_movies = db.session.query(
        Movie.id, Movie.title, Movie.poster_url, Movie.rating,
        func.count(UserBehavior.id).label('click_count')
    ).outerjoin(UserBehavior, UserBehavior.movie_id == Movie.id
                ).filter(Movie.is_blocked == False
                         ).group_by(Movie.id
                                    ).order_by(desc('click_count'), Movie.rating.desc()).limit(20).all()

    # 2. 如果有最近行为，找相似类型电影（简单：同类型的随机）
    similar_movies = []
    if recent_movie_ids:
        # 获取用户最近看过电影的类型
        recent_movies = Movie.query.filter(Movie.id.in_(recent_movie_ids)).all()
        genre_ids = set()
        for m in recent_movies:
            for g in m.genres:
                genre_ids.add(g.id)
        if genre_ids:
            similar_movies = Movie.query.filter(
                Movie.is_blocked == False,
                Movie.genres.any(Genre.id.in_(genre_ids)),
                ~Movie.id.in_(recent_movie_ids)  # 排除已看过的
            ).order_by(func.random()).limit(10).all()

    # 合并去重
    recommended = []
    seen_ids = set()
    # 先加热门
    for m in popular_movies:
        if m.id not in seen_ids:
            recommended.append({
                'id': m.id,
                'title': m.title,
                'poster_url': m.poster_url,
                'rating': m.rating,
                'reason': '热门推荐'
            })
            seen_ids.add(m.id)
    # 再加相似
    for m in similar_movies:
        if m.id not in seen_ids:
            recommended.append({
                'id': m.id,
                'title': m.title,
                'poster_url': m.poster_url,
                'rating': m.rating,
                'reason': '根据您的观影历史'
            })
            seen_ids.add(m.id)

    # 如果不足10个，补一些随机
    if len(recommended) < 10:
        need = 10 - len(recommended)
        random_movies = Movie.query.filter(
            Movie.is_blocked == False,
            ~Movie.id.in_(seen_ids)
        ).order_by(func.random()).limit(need).all()
        for m in random_movies:
            recommended.append({
                'id': m.id,
                'title': m.title,
                'poster_url': m.poster_url,
                'rating': m.rating,
                'reason': '你可能感兴趣'
            })

    return jsonify(recommended[:10])


# 记录用户点击/观看行为
@recommendations_bp.route('/click', methods=['POST'])
@jwt_required()
def record_click():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': '用户不存在'}), 404

    data = request.get_json()
    movie_id = data.get('movie_id')
    behavior_type = data.get('behavior_type', 'click')  # click, view

    behavior = UserBehavior(
        user_id=user.id,
        movie_id=movie_id,
        behavior_type=behavior_type
    )
    db.session.add(behavior)
    db.session.commit()
    return jsonify({'msg': '记录成功'})


# 管理员接口：获取推荐算法配置
@recommendations_bp.route('/config', methods=['GET'])
@jwt_required()
def get_config():
    configs = RecommendationConfig.query.all()
    return jsonify([{
        'id': c.id,
        'algorithm': c.algorithm,
        'weight': c.weight,
        'enabled': c.enabled
    } for c in configs])


# 管理员接口：更新算法配置
@recommendations_bp.route('/config/<int:config_id>', methods=['PUT'])
@jwt_required()
def update_config(config_id):
    config = RecommendationConfig.query.get_or_404(config_id)
    data = request.get_json()
    config.weight = data.get('weight', config.weight)
    config.enabled = data.get('enabled', config.enabled)
    db.session.commit()
    return jsonify({'msg': '更新成功'})


# 管理员接口：人工干预（屏蔽/置顶电影）
@recommendations_bp.route('/intervention', methods=['POST'])
@jwt_required()
def add_intervention():
    data = request.get_json()
    movie_id = data.get('movie_id')
    action = data.get('action')  # 'block' or 'sticky'
    expire_at = None
    if data.get('expire_at'):
        expire_at = datetime.strptime(data['expire_at'], '%Y-%m-%d %H:%M:%S')

    intervention = ManualIntervention(
        movie_id=movie_id,
        action=action,
        expire_at=expire_at
    )
    db.session.add(intervention)

    # 同时更新电影的屏蔽/置顶状态
    movie = Movie.query.get(movie_id)
    if movie:
        if action == 'block':
            movie.is_blocked = True
        elif action == 'sticky':
            movie.is_sticky = True

    db.session.commit()
    return jsonify({'msg': '干预成功'})