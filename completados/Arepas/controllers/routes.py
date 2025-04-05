from flask import request, jsonify

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')

    if len(username) <= 3 or len(password) <= 3:
        return jsonify({"error": "Username and password must be longer than 3 characters"}), 400

    return jsonify({"message": "Login successful"})
