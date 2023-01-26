from flask import request
from . import api
from app.models import User


# Endpoint to create a new user
@api.route('/users/create', methods=['POST'])
def create_user():
    # Check to see that the request sent a JSON request body
    if not request.is_json:
        return {"error": "Missing JSON in request"}, 400
    # Get the data from the request body
    data = request.json

    # Check to see that the data is valid
    for field in ['email', 'username', 'password']:
        if field not in data:
            return {f"error: Missing field: ${field} "}, 400

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    new_user = User(email=email, username=username, password=password)
   

    return new_user.to_dict(), 201

# Endpoint to get an existing user
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user.to_dict(), 200