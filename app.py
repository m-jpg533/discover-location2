from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB = "location.db"

# 🔥 初始化資料庫
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            address TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 🟢 手機頁（傳位置）
@app.route('/')
def index():
    return render_template('track.html')

# 🔵 地圖頁
@app.route('/map')
def map_page():
    return render_template('map.html')

# 📍 存位置 + 地址
@app.route('/save-location', methods=['POST'])
def save_location():
    data = request.get_json()

    lat = data.get("latitude")
    lng = data.get("longitude")
    address = data.get("address")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO locations (latitude, longitude, address) VALUES (?, ?, ?)",
        (lat, lng, address)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# 📡 取得資料
@app.route('/get-locations')
def get_locations():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT latitude, longitude, address
        FROM locations
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"lat": r[0], "lng": r[1], "address": r[2]}
        for r in rows
    ])

# 🚀 Render 用
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
