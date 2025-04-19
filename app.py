from flask import Flask, render_template, request, redirect, url_for, session
import random
import os
import sqlite3
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于管理session

# 图片路径
IMAGE_FOLDER = 'static/images'
IMAGE_FILES = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]

# 随机选择一张图片
def get_random_image():
    return random.choice(IMAGE_FILES)

# 创建数据库和表
def create_db():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 在程序启动时调用 create_db 函数
create_db()



# 检查单词是否已经存在
def word_exists(word):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM user_words WHERE word = ?', (word,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# 保存单词到数据库
def save_word(word):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_words (word) VALUES (?)', (word,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # 如果session中没有图片路径，则随机选择一张
    if 'image' not in session:
        session['image'] = get_random_image()
    return render_template('index.html', image=session['image'])

@app.route('/new_image')
def new_image():
    # 更新session中的图片路径
    session['image'] = get_random_image()
    return redirect(url_for('index'))

@app.route('/learn', methods=['POST'])
def learn():
    words = [request.form.get(f'word{i}') for i in range(1, 6)]
    words = [word.strip() for word in words if word.strip()]
    if len(words) < 1 or len(words) > 5:
        return "Please enter between 1 and 5 words.", 400
    for word in words:
        save_word(word)
    return render_template('learn.html', words=words, image=session['image'])

@app.route('/my_words')
def my_words():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM user_words')
    words = cursor.fetchall()
    conn.close()
    return render_template('my_words.html', words=words)

@app.route('/clear_words', methods=['GET'])
def clear_words():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_words')  # 删除表中的所有数据
    conn.commit()
    conn.close()
    return redirect(url_for('index'))  # 重定向到首页

if __name__ == '__main__':
    app.run(debug=True, port=5001)