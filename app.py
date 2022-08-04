"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_redirect():
    return redirect('/users')

@app.route('/users')
def home():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user():
    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    if(not image_url):
        image_url = None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/users/{new_user.id}")

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    image_url = request.form['image-url']
    if(image_url):
        user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit-form.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('post-form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    tag = request.form.getlist('tags')
    tag_list = [int(i) for i in tag]
    tags = Tag.query.filter(Tag.id.in_(tag_list)).all()

    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/posts/{new_post.id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post-details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']

    tag = request.form.getlist('tags')
    tag_list = [int(i) for i in tag]
    tags = Tag.query.filter(Tag.id.in_(tag_list)).all()

    if(title):
        post.title = title
    if(content):
        post.content = content
    if(tags):
        post.tags = tags
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-details.html', tag=tag)

@app.route('/tags/new')
def show_tag_form():
    posts = Post.query.all()
    return render_template('tag-form.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def new_tag():
    name = request.form['name']

    post = request.form.getlist('tags')
    post_list = [int(i) for i in post]
    posts = Post.query.filter(Post.id.in_(post_list)).all()

    new_tag = Tag(name=name, posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit-tag.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']
    post = request.form.getlist('tags')
    post_list = [int(i) for i in post]
    posts = Tag.query.filter(Tag.id.in_(post_list)).all()

    if(name):
        tag.name = name
    if(posts):
        tag.posts = posts

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')


