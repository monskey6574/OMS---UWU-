from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY, product TEXT, quantity INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    data = request.json
    product = data.get('product')
    quantity = data.get('quantity')
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("UPDATE inventory SET quantity = quantity - ? WHERE product = ?", (quantity, product))
    conn.commit()
    conn.close()
    return jsonify({"message": "Inventory updated"})

if __name__ == '__main__':
    app.run(port=5002)