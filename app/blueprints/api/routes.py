from flask import request
from . import api
from app.models import Post, User

#####################
#        Post       #
#####################

@api.route('/')
def index():
    return 'Hello this is the api'

# Endpoint to get ALL of the posts
@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return [p.to_dict() for p in posts]

# Endpoint to  get a single post
@api.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post.to_dict()


# Endpoint to create new post
@api.route('/posts', methods=['POST'])
def create_post():
    # ChecK to see that the request sent a request body that is JSON
    if not request.is_json:
        return {"error": "Missing JSON in request"}, 400
    # Get the data from the request body
    data = request.json

    # Check to see that the data is valid
    for field in ['title', 'body', 'user_id']:
        if field not in data:
             # If the field is not in the request body, throw an error saying they are missing that field
            return {"error": "Missing field: " + field}, 400
    
    # pull the fields from the request data
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')

     # Create a new Post instance with data from request
    new_post = Post(title=title, body=body, user_id=user_id)

    # Return the new post as a JSON response
    return new_post.to_dict(), 201


#####################
#        User       #
#####################

# Endpoint to create a new user
@api.route('/users', methods=['POST'])
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
    # pull values from rquest body
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter((User.User.username == username) | (User.email == email)).all()
    if existing_user:
        return {f"error: User already exists"}, 400

    #create new user instance
    new_user = User(email=email, username=username, password=password)
    
    return new_user.to_dict(), 201

# Endpoint to get an existing user
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user.to_dict(), 200
 
# Endpoint to get all users
# @api.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.filter_by(username=username)
#     return [user.to_dict() for user in users], 200