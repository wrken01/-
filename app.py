# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'a_random_secret_key'  # Flask flash 消息需要

# 上传文件相关配置
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """判断文件是否是允许的图片格式"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 物品登记页面（表单）
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item_name = request.form['item_name']         # 物品名称
        quantity = request.form['quantity']           # 数量
        repair_person = request.form['repair_person'] # 维修人
        file = request.files['image']                 # 上传的图片文件

        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # 防止恶意文件名
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

        if item_name and quantity and repair_person:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO items_log (item_name, quantity, repair_person, image_path)
                VALUES (%s, %s, %s, %s)
            """, (item_name, quantity, repair_person, image_path))
            conn.commit()
            cursor.close()
            conn.close()

            flash("✅ 登记成功！")
            return redirect('/')
        else:
            flash("❌ 请填写完整信息")
            return redirect('/')

    return render_template('form.html')

# 物品查询页面
@app.route('/query', methods=['GET'])
def query_items():
    keyword = request.args.get('keyword', '')  # 搜索关键字（可为空）

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # dictionary=True → 返回字典格式，方便模板渲染

    if keyword:
        sql = """
            SELECT * FROM items_log
            WHERE item_name LIKE %s OR repair_person LIKE %s
            ORDER BY id DESC
        """
        cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
    else:
        sql = "SELECT * FROM items_log ORDER BY id DESC"
        cursor.execute(sql)

    items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('query.html', items=items, keyword=keyword)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
