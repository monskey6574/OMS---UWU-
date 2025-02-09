from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('shipment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS shipments
                 (id INTEGER PRIMARY KEY, order_id INTEGER, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/create_shipment', methods=['POST'])
def create_shipment():
    data = request.json
    order_id = data.get('order_id')
    conn = sqlite3.connect('shipment.db')
    c = conn.cursor()
    c.execute("INSERT INTO shipments (order_id, status) VALUES (?, ?)", (order_id, 'pending'))
    conn.commit()
    conn.close()
    return jsonify({"order_id": order_id, "status": "pending"})

@app.route('/shipment_status/<int:order_id>', methods=['GET'])
def shipment_status(order_id):
    conn = sqlite3.connect('shipment.db')
    c = conn.cursor()
    c.execute("SELECT status FROM shipments WHERE order_id=?", (order_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return jsonify({"order_id": order_id, "status": result[0]})
    return jsonify({"error": "Shipment not found"}), 404

if __name__ == '__main__':
    app.run(port=5004)