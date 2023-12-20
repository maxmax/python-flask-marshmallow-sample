from flask import Flask, request, jsonify
from marshmallow import Schema, fields
import json

app = Flask(__name__)

class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.Email()

user_schema = UserSchema()
users = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "johndoe@example.com"
    },
    {
        "id": 2,
        "name": "Jane Doe",
        "email": "janedoe@example.com"
    }
]

@app.route('/users/', methods=['GET'])
def get_users():
    return jsonify(user_schema.dump(users, many=True))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user_schema.dump(user))
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    new_user = user_schema.load(user_data, partial=True)
    users.append(new_user)
    return jsonify(user_schema.dump(new_user)), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        user_data = request.get_json()
        updated_user = user_schema.load(user_data, partial=True)
        user.update(updated_user)
        return jsonify(user_schema.dump(user))
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        users.remove(user)
        return jsonify({"success": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
