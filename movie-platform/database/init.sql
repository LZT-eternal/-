-- 用户表
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    register_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    last_login DATETIME COMMENT '最后登录时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0禁用，1启用',
    gender ENUM('男','女','其他') COMMENT '性别',
    age INT COMMENT '年龄',
    region VARCHAR(100) COMMENT '地区',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 角色表
CREATE TABLE role (
    role_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '角色ID',
    role_name VARCHAR(50) NOT NULL UNIQUE COMMENT '角色名称',
    description TEXT COMMENT '角色描述',   -- 改为 TEXT 避免长度限制
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- 权限表
CREATE TABLE permission (
    permission_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '权限ID',
    permission_name VARCHAR(50) NOT NULL COMMENT '权限名称',
    permission_key VARCHAR(100) NOT NULL UNIQUE COMMENT '权限标识符',
    parent_id INT COMMENT '父权限ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES permission(permission_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

-- 菜单表
CREATE TABLE menu (
    menu_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '菜单ID',
    menu_name VARCHAR(50) NOT NULL COMMENT '菜单名称',
    parent_id INT COMMENT '父菜单ID',
    url VARCHAR(200) COMMENT '菜单链接',
    permission_key VARCHAR(100) COMMENT '关联的权限标识符',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES menu(menu_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_key) REFERENCES permission(permission_key) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='菜单表';

-- 用户角色关联表
CREATE TABLE user_role (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE CASCADE   -- 修正为 role_id
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户角色关联表';

-- 角色权限关联表
CREATE TABLE role_permission (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE CASCADE,   -- 修正为 role_id
    FOREIGN KEY (permission_id) REFERENCES permission(permission_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色权限关联表';

-- 电影类型表
CREATE TABLE genre (
    genre_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '类型ID',
    genre_name VARCHAR(50) NOT NULL UNIQUE COMMENT '类型名称',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影类型表';

-- 影人表
CREATE TABLE celebrity (
    celebrity_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '影人ID',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    gender ENUM('男','女','其他') COMMENT '性别',
    birth_date DATE COMMENT '出生日期',
    nationality VARCHAR(50) COMMENT '国籍',
    biography TEXT COMMENT '简介',
    photo_url VARCHAR(500) COMMENT '照片URL',
    is_blocked TINYINT NOT NULL DEFAULT 0 COMMENT '是否屏蔽：0否，1是',
    is_pinned TINYINT NOT NULL DEFAULT 0 COMMENT '是否置顶：0否，1是',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='影人表';

-- 电影表
CREATE TABLE movie (
    movie_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '电影ID',
    title VARCHAR(200) NOT NULL COMMENT '片名',
    description TEXT COMMENT '简介',
    release_date DATE COMMENT '上映日期',
    duration INT COMMENT '片长（分钟）',
    language VARCHAR(50) COMMENT '语言',
    country VARCHAR(50) COMMENT '国家',
    poster_url VARCHAR(500) COMMENT '海报URL',
    rating DECIMAL(2,1) DEFAULT 0.0 COMMENT '评分',
    is_blocked TINYINT NOT NULL DEFAULT 0 COMMENT '是否屏蔽：0否，1是',
    is_pinned TINYINT NOT NULL DEFAULT 0 COMMENT '是否置顶：0否，1是',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影表';

-- 电影类型关联表
CREATE TABLE movie_genre (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影类型关联表';

-- 电影影人关联表
CREATE TABLE movie_celebrity (
    movie_id INT NOT NULL,
    celebrity_id INT NOT NULL,
    job_type ENUM('导演','演员','编剧','制片') NOT NULL COMMENT '职务类型',
    character_name VARCHAR(100) COMMENT '扮演角色（当职务为演员时填写）',
    PRIMARY KEY (movie_id, celebrity_id, job_type),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (celebrity_id) REFERENCES celebrity(celebrity_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电影影人关联表';

-- 用户行为表
CREATE TABLE user_behavior (
    behavior_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '行为ID',
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    behavior_type ENUM('评分','评论','收藏') NOT NULL COMMENT '行为类型',
    content TEXT COMMENT '评论内容',
    rating INT COMMENT '评分',
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '行为时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_movie (movie_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户行为表';

-- 票房表
CREATE TABLE box_office (
    boxoffice_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '票房记录ID',
    movie_id INT NOT NULL,
    date DATE NOT NULL COMMENT '日期',
    region VARCHAR(100) NOT NULL COMMENT '地区',
    amount DECIMAL(12,2) NOT NULL DEFAULT 0.00 COMMENT '票房金额',
    screenings INT NOT NULL DEFAULT 0 COMMENT '排片场次',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    UNIQUE KEY uk_movie_date_region (movie_id, date, region),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='票房表';

-- 算法配置表
CREATE TABLE algorithm_config (
    config_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '配置ID',
    algorithm_name VARCHAR(50) NOT NULL UNIQUE COMMENT '算法名称',
    parameters JSON COMMENT '算法参数（JSON格式）',
    enabled TINYINT NOT NULL DEFAULT 1 COMMENT '是否启用：0否，1是',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推荐算法配置表';

-- 推荐结果表
CREATE TABLE recommendation (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '推荐ID',
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    reason VARCHAR(255) COMMENT '推荐理由',
    algorithm VARCHAR(50) COMMENT '使用的算法',
    generated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
    clicked TINYINT NOT NULL DEFAULT 0 COMMENT '是否点击：0否，1是',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_generated (generated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='推荐结果表';

-- 日志表
CREATE TABLE log (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    user_id INT COMMENT '操作用户ID',
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    action VARCHAR(100) NOT NULL COMMENT '操作动作',
    content TEXT COMMENT '操作内容',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    result VARCHAR(10) COMMENT '操作结果',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统操作日志表';

-- 系统配置表
CREATE TABLE system_config (
    config_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '配置ID',
    param_key VARCHAR(100) NOT NULL UNIQUE COMMENT '参数键',
    param_value TEXT NOT NULL COMMENT '参数值',
    description TEXT COMMENT '描述',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

-- 插入基础数据（按依赖顺序）
-- 角色
INSERT INTO role (role_name, description) VALUES
('管理员', '系统管理员，拥有所有权限'),
('普通用户', '普通注册用户');

-- 权限（示例）
INSERT INTO permission (permission_name, permission_key, parent_id) VALUES
('用户管理', 'user:manage', NULL),
('电影管理', 'movie:manage', NULL),
('影人管理', 'celebrity:manage', NULL);

-- 菜单（示例）
INSERT INTO menu (menu_name, url, permission_key, sort_order) VALUES
('电影管理', '/admin/movies', 'movie:manage', 1),
('影人管理', '/admin/celebrities', 'celebrity:manage', 2),
('用户管理', '/admin/users', 'user:manage', 3);

-- 角色权限关联（为管理员分配所有权限）
INSERT INTO role_permission (role_id, permission_id)
SELECT 1, permission_id FROM permission;

-- 用户（密码哈希使用 generate_password_hash 生成，这里用占位符，实际需替换）
-- 注意：密码哈希需要实际生成，这里仅为示例，测试时可使用硬编码账号（无需此数据）
INSERT INTO user (username, password_hash, email, phone) VALUES
('admin', 'pbkdf2:sha256:260000$...', 'admin@example.com', '13800138000'),
('user', 'pbkdf2:sha256:260000$...', 'user@example.com', '13900139000');

-- 用户角色关联
INSERT INTO user_role (user_id, role_id) VALUES
(1, 1), (2, 2);

-- 电影类型
INSERT INTO genre (genre_name) VALUES
('剧情'), ('喜剧'), ('动作'), ('科幻'), ('爱情');

-- 示例电影（可选）
INSERT INTO movie (title, release_date, duration, language, country, rating) VALUES
('示例电影1', '2025-01-01', 120, '国语', '中国', 8.5),
('示例电影2', '2025-02-01', 110, '英语', '美国', 7.8);

-- 电影类型关联
INSERT INTO movie_genre (movie_id, genre_id) VALUES
(1, 1), (1, 3), (2, 2), (2, 4);