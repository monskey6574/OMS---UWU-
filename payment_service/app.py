from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    amount = data.get('amount')
    # Simulate payment processing
    if amount > 0:
        return jsonify({"status": "success", "message": "Payment processed"})
    return jsonify({"status": "failed", "message": "Invalid amount"}), 400

if __name__ == '__main__':
    app.run(port=5003)