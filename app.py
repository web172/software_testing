import time

from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
app = Flask(__name__)
# 模拟库存
app.secret_key = 'your_secret_key_here'
inventory = {"book": 10}

# ---------------------- 数据库配置（与 docker-compose.yml 一致）----------------------
DB_CONFIG = {
    "user": "test_user",
    "password": "123456",
    "host": "localhost",  # 本地 Docker 容器，用 localhost 即可
    "port": "3306",
    "db": "order_db"
}
# 创建数据库连接引擎
engine_url = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db']}"
engine = create_engine(engine_url, pool_recycle=300)  # 避免连接超时


# ---------------------- 初始化数据库表（首次启动自动创建订单表）----------------------
def init_db():
    try:
        # 连接数据库并创建 orders 表
        with engine.connect() as conn:
            create_table_sql = """
                               CREATE TABLE IF NOT EXISTS orders \
                               ( \
                                   id \
                                   INT \
                                   AUTO_INCREMENT \
                                   PRIMARY \
                                   KEY, \
                                   item \
                                   VARCHAR \
                               ( \
                                   50 \
                               ) NOT NULL,
                                   qty INT NOT NULL,
                                   create_time DATETIME DEFAULT CURRENT_TIMESTAMP
                                   ); \
                               """
            conn.execute(text(create_table_sql))
            conn.commit()
        print("数据库表初始化成功（orders 表已创建/存在）")
    except OperationalError as e:
        print(f"初始化数据库失败：{e}（可能数据库未启动，稍后重试）")
        time.sleep(2)
        init_db()  # 重试（避免服务启动快于数据库）


# ---------------------- /order 接口（处理订单提交）----------------------


@app.route("/order", methods=["POST"])
def order():
    item = request.json.get("item")
    qty = request.json.get("qty", 1)
    if item not in inventory:
        return jsonify({"error": "不存在的商品"}), 400
    if inventory[item] < qty:
        return jsonify({"error": "库存不足"}), 400
    inventory[item] -= qty
    return jsonify({"success": True,"剩余库存": inventory[item]})
@app.route('/')
def index():
    # 检查用户是否已登录（通过session判断）
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    # 未登录则重定向到登录页
    flash('请先登录', 'warning')
    return redirect(url_for('login'))

# 登录页面路由（支持GET和POST方法）
USER_DATA = {
    'admin': '123456',  # 用户名: 密码（实际需加密存储）
    'user1': 'abc123'
}
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单提交的用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 验证用户信息
        if username in USER_DATA and USER_DATA[username] == password:
            # 登录成功：将用户名存入session
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('index'))  # 重定向到首页
        else:
            # 登录失败：显示错误提示
            flash('用户名或密码错误，请重新输入', 'danger')
            return redirect(url_for('login'))  # 重新显示登录页
    
    # GET请求：显示登录页面
    return render_template('login.html')

@app.route("/order1", methods=["POST"])
def create_order():
    try:
        # 获取请求参数
        data = request.get_json()
        item = data.get("item")
        qty = data.get("qty")

        # 校验参数
        if not item or not qty or not isinstance(qty, int):
            return jsonify({"error": "参数错误（item 不能为空，qty 必须为整数）"}), 400

        # 插入订单到数据库
        with engine.connect() as conn:
            insert_sql = text("INSERT INTO orders (item, qty) VALUES (:item, :qty)")
            conn.execute(insert_sql, {"item": item, "qty": qty})
            conn.commit()

        return jsonify({"message": "订单创建成功", "order": {"item": item, "qty": qty}}), 200

    # 捕获数据库连接错误（如数据库停掉）
    except OperationalError as e:
        print(f"数据库错误：{e}")
        return jsonify({"error": "数据库服务不可用"}), 503  # 返回 503（服务不可用），符合测试断言

    # 其他未知错误
    except Exception as e:
        print(f"未知错误：{e}")
        return jsonify({"error": "服务器内部错误"}), 500  # 返回 500，符合测试断言

if __name__ == "__main__":
    init_db()  # 启动前初始化数据库表
    # 监听 127.0.0.1:5000（与测试代码请求地址一致）
    app.run(host="127.0.0.1", port=5000, debug=True)
