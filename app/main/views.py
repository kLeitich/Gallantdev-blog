from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Role,Blog,Comment
from flask_login import current_user, login_required
from .forms import  NewComment, UpdateProfile,NewBlog
from .. import db,photos


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    # blogs = Blog.query.all()
    return render_template('index.html')




@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/blog/<uname>/update',methods = ['GET','POST'])
@login_required
def new_blog(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = NewBlog()

    if form.validate_on_submit():
        category = form.category.data
        blogContent = form.blogContent.data
        blogAuthor = form.blogAuthor.data
        new_blog = Blog(category=category,blogContent=blogContent,blogAuthor=blogAuthor)
        
        new_blog.save_blog()
        return redirect(url_for('main.index',uname=user.username))
    

   
    return render_template('blog.html',form =form)


@main.route('/comment/<uname>/update',methods = ['GET','POST'])
@login_required
def new_comment(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = NewComment()

    if form.validate_on_submit():
        comment= form.commentNew.data
        comment_author=form.comment_author.data
        new_comment = Comment(comment=comment,comment_author=comment_author)

        new_comment.save_comment()
        return redirect(url_for('main.new_comment',uname=user.username))

    comments = Comment.query.all()
    

    return render_template('comment.html',form =form,comments=comments)


@main.route('/category/story')
def interview():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('category/story.html')


@main.route('/category/tech')
def product():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('category/tech.html')

@main.route('/category/articles')
def promotion():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('category/articles.html')

@main.route('/category/personal')
def sales():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('category/personal.html')



