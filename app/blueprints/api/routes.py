from flask import request
from . import api
from app.models import Post

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
            return {"error": "Missing field: " + field}, 400
    

    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')

    new_post = Post(title=title, body=body, user_id=user_id)

    return new_post.to_dict(), 201
