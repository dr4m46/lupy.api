from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database simulation
users_db = {
    "test@email.com": {
        "password": "test123", 
        "data": {"money": 1000, "coins": 50, "rank": 5}
    }
}

@app.route('/')
def home():
    return jsonify({
        "message": "LUPY7 API IS LIVE!",
        "version": "1.0",
        "endpoints": [
            "/api/login",
            "/api/get_data", 
            "/api/set_money"
        ]
    })

@app.route('/api/account_login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('account_email')
    password = data.get('account_password')
    
    if email in users_db and users_db[email]['password'] == password:
        return jsonify({
            "ok": True, 
            "auth": f"lupy_token_{email}",
            "error": 0
        })
    return jsonify({"error": 1, "message": "Login failed"})

@app.route('/api/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    auth_token = data.get('account_auth')
    
    if auth_token and auth_token.startswith('lupy_token_'):
        email = auth_token.replace('lupy_token_', '')
        return jsonify({"ok": True, "data": users_db[email]['data']})
    return jsonify({"error": 2, "message": "Invalid token"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
