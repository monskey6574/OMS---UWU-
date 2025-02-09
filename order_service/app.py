from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('order.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY, items TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json
    items = data.get('items')
    conn = sqlite3.connect('order.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (items, status) VALUES (?, ?)", (items, 'created'))
    conn.commit()
    order_id = c.lastrowid
    conn.close()
    return jsonify({"order_id": order_id, "status": "created"})

@app.route('/order_status/<int:order_id>', methods=['GET'])
def order_status(order_id):
    conn = sqlite3.connect('order.db')
    c = conn.cursor()
    c.execute("SELECT status FROM orders WHERE id=?", (order_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return jsonify({"order_id": order_id, "status": result[0]})
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(port=5001)