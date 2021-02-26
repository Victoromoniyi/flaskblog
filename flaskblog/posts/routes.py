from flask import (Blueprint, render_template, url_for,
flash, redirect, abort)
from flask_login import current_user, login_required, current_user
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import PostForm, CommentForm


posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Success! Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('make_post.html', title='New Post',form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['POST', 'GET'])
def post(post_id):
     post = Post.query.get_or_404(post_id)
     comments = Comment.query.filter(Comment.post_id == post.id)
     form = CommentForm()
     return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@posts.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) #Manual HTTP 403. Forbidden Route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect (url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.content.data = post.content
        form.title.data = post.title
    return render_template('make_post.html', title='Edit Post',form=form, legend='Edit Post')

@posts.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data, post_id=post.id, author_id=current_user.id))
        db.session.commit()
        flash("Your comment has been submitted", "success")
        return redirect(f'/post/{post.id}')

        comments = Comment.query.filter(Comment.post_id == post.id)
        return render_template('post.html', post=post, comments=comments, form=form)

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect (url_for('main.home'))
