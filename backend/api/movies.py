from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from models import db, Movie, Genre, User, user_favorites
from auth import admin_required

movies_bp = Blueprint('movies', __name__, url_prefix='/api/movies')


# 公开接口：获取电影列表（支持分页、搜索、筛选）
@movies_bp.route('/', methods=['GET'])
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    title = request.args.get('title', '')
    genre_id = request.args.get('genre_id', type=int)
    year = request.args.get('year', type=int)

    query = Movie.query.filter_by(is_blocked=False)  # 默认不显示屏蔽电影

    if title:
        query = query.filter(Movie.title.contains(title))
    if genre_id:
        query = query.filter(Movie.genres.any(id=genre_id))
    if year:
        query = query.filter(db.extract('year', Movie.release_date) == year)

    # 按置顶和时间排序
    query = query.order_by(Movie.is_sticky.desc(), Movie.release_date.desc())

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    movies = []
    for movie in paginated.items:
        movies.append({
            'id': movie.id,
            'title': movie.title,
            'poster_url': movie.poster_url,
            'rating': movie.rating,
            'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None,
            'genres': [{'id': g.id, 'name': g.name} for g in movie.genres]
        })

    return jsonify({
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'data': movies
    })


# 公开接口：获取单个电影详情
@movies_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie.is_blocked:
        return jsonify({'msg': '电影已屏蔽'}), 404

    # 获取影人信息
    celebrities = []
    for mc in movie.celebrities:
        celebrities.append({
            'id': mc.celebrity_id,
            'name': mc.celebrity.name,
            'role': mc.role,
            'character': mc.character,
            'photo_url': mc.celebrity.photo_url
        })

    data = {
        'id': movie.id,
        'title': movie.title,
        'original_title': movie.original_title,
        'description': movie.description,
        'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None,
        'duration': movie.duration,
        'language': movie.language,
        'country': movie.country,
        'poster_url': movie.poster_url,
        'rating': movie.rating,
        'genres': [{'id': g.id, 'name': g.name} for g in movie.genres],
        'celebrities': celebrities,
        'is_sticky': movie.is_sticky
    }
    return jsonify(data)


# 需要登录：收藏/取消收藏
@movies_bp.route('/<int:movie_id>/favorite', methods=['POST'])
@jwt_required()
def toggle_favorite(movie_id):
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': '用户不存在'}), 404

    movie = Movie.query.get_or_404(movie_id)

    # 检查是否已收藏
    if movie in user.favorites:
        user.favorites.remove(movie)
        db.session.commit()
        return jsonify({'favorite': False})
    else:
        user.favorites.append(movie)
        db.session.commit()
        return jsonify({'favorite': True})


# 需要登录：获取用户收藏列表
@movies_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': '用户不存在'}), 404

    movies = []
    for movie in user.favorites:
        movies.append({
            'id': movie.id,
            'title': movie.title,
            'poster_url': movie.poster_url,
            'rating': movie.rating,
            'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None
        })
    return jsonify(movies)


# 管理员接口：新增电影
@movies_bp.route('/', methods=['POST'])
@admin_required
def create_movie():
    data = request.get_json()
    movie = Movie(
        title=data['title'],
        original_title=data.get('original_title'),
        description=data.get('description'),
        release_date=datetime.strptime(data['release_date'], '%Y-%m-%d') if data.get('release_date') else None,
        duration=data.get('duration', type=int),
        language=data.get('language'),
        country=data.get('country'),
        poster_url=data.get('poster_url'),
        rating=data.get('rating', type=float),
        is_blocked=data.get('is_blocked', False),
        is_sticky=data.get('is_sticky', False)
    )

    # 处理类型
    genre_ids = data.get('genre_ids', [])
    for gid in genre_ids:
        genre = Genre.query.get(gid)
        if genre:
            movie.genres.append(genre)

    db.session.add(movie)
    db.session.commit()
    return jsonify({'id': movie.id, 'msg': '创建成功'}), 201


# 管理员接口：更新电影
@movies_bp.route('/<int:movie_id>', methods=['PUT'])
@admin_required
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    data = request.get_json()

    movie.title = data.get('title', movie.title)
    movie.original_title = data.get('original_title', movie.original_title)
    movie.description = data.get('description', movie.description)
    if data.get('release_date'):
        movie.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d')
    movie.duration = data.get('duration', movie.duration)
    movie.language = data.get('language', movie.language)
    movie.country = data.get('country', movie.country)
    movie.poster_url = data.get('poster_url', movie.poster_url)
    movie.rating = data.get('rating', movie.rating)
    movie.is_blocked = data.get('is_blocked', movie.is_blocked)
    movie.is_sticky = data.get('is_sticky', movie.is_sticky)

    # 更新类型：先清空再添加
    if 'genre_ids' in data:
        movie.genres = []
        for gid in data['genre_ids']:
            genre = Genre.query.get(gid)
            if genre:
                movie.genres.append(genre)

    db.session.commit()
    return jsonify({'msg': '更新成功'})


# 管理员接口：删除电影
@movies_bp.route('/<int:movie_id>', methods=['DELETE'])
@admin_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'msg': '删除成功'})


# 公开接口：获取所有类型（用于筛选）
@movies_bp.route('/genres', methods=['GET'])
def get_genres():
    genres = Genre.query.all()
    return jsonify([{'id': g.id, 'name': g.name} for g in genres])


# 公开接口：获取年份列表（用于筛选）
@movies_bp.route('/years', methods=['GET'])
def get_years():
    years = db.session.query(db.extract('year', Movie.release_date)).distinct().order_by(
        db.extract('year', Movie.release_date).desc()).all()
    return jsonify([int(y[0]) for y in years if y[0] is not None])