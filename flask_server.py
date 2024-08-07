from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

def load_users():
    if not os.path.exists('users.json'):
        return {}
    with open('users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_or_login', methods=['POST'])
def register_or_login():
    data = request.get_json()
    user_id = str(data['user_id'])
    user_name = data['user_name']

    users = load_users()

    if user_id not in users:
        users[user_id] = {
            'name': user_name,
            'tokens': 0,
            'tokens_per_minute': 0,
            'price_per_token_minute': 100,
            'tokens_per_minute_value': 1,
            'bought_token_per_minute': False,
            'level': 1  # Adiciona nível inicial
        }
        save_users(users)
        return jsonify(success=True, user_data=users[user_id], message="New user registered")
    else:
        return jsonify(success=True, user_data=users[user_id], message="User logged in")

@app.route('/update_tokens', methods=['POST'])
def update_tokens():
    data = request.get_json()
    user_id = str(data['user_id'])
    tokens = int(data['tokens'])
    tokens_per_minute = int(data['tokens_per_minute'])
    price_per_token_minute = int(data['price_per_token_minute'])
    tokens_per_minute_value = int(data['tokens_per_minute_value'])
    bought_token_per_minute = data['bought_token_per_minute']
    level = int(data['level'])  # Adiciona o nível

    users = load_users()

    if user_id in users:
        users[user_id]['tokens'] = max(0, tokens)
        users[user_id]['tokens_per_minute'] = max(0, tokens_per_minute)
        users[user_id]['price_per_token_minute'] = max(0, price_per_token_minute)
        users[user_id]['tokens_per_minute_value'] = max(0, tokens_per_minute_value)
        users[user_id]['bought_token_per_minute'] = bought_token_per_minute
        users[user_id]['level'] = level  # Atualiza o nível
        save_users(users)
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="User not found")

if __name__ == '__main__':
    app.run(port=8000)
