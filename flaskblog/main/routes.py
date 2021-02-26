from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route('/')
@main.route('/home2')
def home_asc():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.asc()).paginate(page=page, per_page=5)
    return render_template('homeasc.html', posts=posts)


@main.route('/search', methods=['GET', 'POST'])
def search():
    s = request.args.get('s')
    if s:
        posts = Post.query.filter(Post.title.contains(s) |
        Post.content.contains(s))
    else:
        posts =  Post.query.all()
    return render_template('search.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/privacypolicy')
def privacy_policy():
    return render_template('privacypolicy.html', title='Privacy Policy')

@main.route('/likedposts')
def liked_posts():
    return render_template('likedposts.html', title='Liked Posts')
