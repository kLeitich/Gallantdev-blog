from os import uname
from app.request import get_qoute
from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Role,Blog,Comment
from flask_login import current_user, login_required
from .forms import  NewComment, UpdateProfile,NewBlog,EmailSubscription
from .. import db,photos


@main.route('/',methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    qoutes=get_qoute()
    form=EmailSubscription()
    blogs = Blog.get_all_blog()
    user=User.query.all()
    print(user)
    # pic=User.query.filter_by(profile_pic_path=profile_pic_path)
  
    return render_template('index.html',blogs=blogs,qoutes=qoutes,user=user,form=form)




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

    return render_template('profile/update.html',form =form,user=user)


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


@main.route('/blog/new',methods = ['GET','POST'])
@login_required
def new_blog():
    # user = User.query.filter_by(username=user_id).first()
    # if user is None:
    #     abort(404)

    form = NewBlog()
    # if category is None:
    #     abort(404)

    if form.validate_on_submit():
        category = form.category.data
        blogTitle=form.blogTitle.data
        blogContent = form.blogContent.data
        user_id=current_user._get_current_object().id
        new_blog = Blog(category=category,blogTitle=blogTitle,blogContent=blogContent,user_id=user_id)
        
        new_blog.save_blog()
        return redirect(url_for('main.index'))
    

   
    return render_template('new_blog.html',form =form,user=current_user)


@main.route('/blog/<int:blog_id>')
def blog(blog_id):

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    found_blog= Blog.get_all_blog(blog_id)
    title = blog_id
    blog_comments = Comment.get_comments(blog_id)

    return render_template('blog.html',title= title ,found_blog= found_blog, blog_comments= blog_comments)


@main.route('/blog/comment/<int:blog_id>',methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    # user = User.query.filter_by(user_id).first()
    # if user is None:
    #     abort(404)
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    print(comments)
    form = NewComment()

    if form.validate_on_submit():
        comment= form.commentNew.data
        user_id=current_user._get_current_object().id
        new_comment = Comment(comment=comment,blog_id=blog_id,user_id=user_id)

        new_comment.save_comment()
        return redirect(url_for('main.new_comment',blog_id=blog_id))
    
    

    return render_template('comment.html',form =form,comments=comments)


# @main.route('/comment/delete/<int:blog_id>',methods = ['GET','POST'])
# @login_required
# def delete_comment(blog_id):
#     # user = User.query.filter_by(blog_id).first()
#     # if user is None:
#     #     abort(404)
#     comments = Comment.query.filter_by(blog_id=blog_id).all()
#     print(comments)
#     user_id=user_id.users.username
#     if current_user==user_id.users.username:
#         delete_comment()
#         comments = Comment.query.all()
#         print(comments)
#         return redirect(url_for('main.delete_comment',uname=user.username))

    
    

#     return render_template('comment.html',form =form,comments=comments)
main.route('/comment/delete/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    
    comments = Comment.query.filter_by(id = comment_id).first()
    if comments.user != current_user:
            return render_template('four.html',message = 'Unauthorized Access')

    for comment in comments:
        db.session.delete(comment)
        db.session.commit()
    
    return redirect(url_for('main.comment',blog_id=comment.blog_id))


@main.route('/story/category')
def story():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('story.html')


@main.route('/tech/category')
def tech():

    '''
    View root page function that returns the index page and its data
    '''
    
    
    return render_template('tech.html')

@main.route('/articles/category')
def articles():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('articles.html')

@main.route('/personal/category')
def personal():

    '''
    View root page function that returns the index page and its data
    '''
    
    return render_template('personal.html')


@main.route('/blog/delete/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    

    if blog.users!= current_user:
         return render_template('fourOwfour.html',message = 'Access denied')

    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/blog/update/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    form = NewBlog()

    if blog.users!= current_user:
         return render_template('fourOwfour.html',message = 'Access denied')
    

    if form.validate_on_submit():
        blog.category = form.category.data
        blog.blogTitle=form.blogTitle.data
        blog.blogContent = form.blogContent.data
        db.session.commit()
        
        
        return redirect(url_for('main.index'))
    
    elif request.method=='GET':
        form.category.data=blog.category 
        form.blogTitle.data=blog.blogTitle
        form.blogContent.data=blog.blogContent



    return render_template('updateblog.html',form=form,blog=blog)



