from portfolio import portfolio, app, mail
from flask import render_template, redirect, url_for, flash, send_file
from portfolio.forms import BlogSignUpForm, MessageForm, CreateOrRemoveBlogForm, CreateOrRemoveProjectForm, EmailForm
from portfolio.models import User, MessageToAdmin, Blog, Projects, Post
from flask_mail import Message

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/download')
def download():
    path = 'C:/Users/Lenovo/Desktop/Personal-Projects/Hackathon-Portfolio-Page/portfolio/static/resume.pdf'
    return send_file(path, as_attachment=True)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    projects = Projects.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/blogs', methods=('GET', 'POST'))
def blogs():
    blog_form = BlogSignUpForm()
    all_blogs = Blog.query.all()
    blog = Blog.query.filter_by(name=blog_form.blog.data).first()
    user = User.query.filter_by(email=blog_form.email.data).first()
    if blog_form.validate_on_submit():
        if user:
            user.blogs.append(blog)
            portfolio.session.commit()
        else:
            user = User(name=blog_form.name.data, email=blog_form.email.data)
            user.blogs.append(blog)
            user.save_user()
        flash(f"You've been signed up for the {blog.name} blog!")
        redirect(url_for('landing_page'))
    return render_template('blogs.html', blog_form=blog_form, all_blogs=all_blogs)

@app.route('/blog/<int:blog_id>', methods=('GET', 'POST'))
def ind_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    blog_form = BlogSignUpForm()
    user = User.query.filter_by(email=blog_form.email.data).first()
    if blog_form.validate_on_submit():
        if user:
            user.blogs.append(blog)
            portfolio.session.commit()
        else:
            user = User(name=blog_form.name.data, email=blog_form.email.data)
            user.blogs.append(blog)
            user.save_user()
        flash(f"You've been signed up for the {blog.name} blog!")
        redirect(url_for('blogs'))
    return render_template('ind_blog.html', blog=blog, blog_form=blog_form)


@app.route('/contact', methods=('GET', 'POST'))
def contact():
    message_form = MessageForm()
    if message_form.validate_on_submit():
        if message_form.name.data == 'Yisroel' and message_form.email.data == 'yisroel.d.baum@gmail.com' and message_form.message.data == 'Yes this is a secret login':
            return redirect(url_for('admin'))
        user = User.query.filter_by(email=message_form.email.data).first()
        if user:
            message_to_send = MessageToAdmin(text=message_form.message.data, user=user)
            message_to_send.save_message()
        else:
            user = User(name=message_form.name.data, email=message_form.email.data)
            user.save_user()
            message_to_send = MessageToAdmin(text=message_form.message.data, user=user)
            message_to_send.save_message()
        return redirect(url_for('contact_confirmation'))
    return render_template('contact.html', message_form=message_form)

@app.route('/contact_confirmation')
def contact_confirmation():
    return render_template('contact_confirmation.html')

@app.route('/delete_message/<message_id>')
def delete_message(message_id):
    message = MessageToAdmin.query.filter_by(id=message_id).first()
    portfolio.session.delete(message)
    portfolio.session.commit()
    return redirect(url_for('admin'))


@app.route('/admin', methods=('GET', 'POST'))
def admin():

    blog_action    = CreateOrRemoveBlogForm()
    project_action = CreateOrRemoveProjectForm()
    email_action   = EmailForm()
    if project_action.validate_on_submit():
        if project_action.action.data == 'Create':
            search_project = Projects.query.filter_by(name=project_action.name.data).first()
            if search_project:
                flash('A project with that name already exists!')
                return redirect(url_for('admin'))
            else:
                project = Projects(name=project_action.name.data, description=project_action.description.data, url=project_action.url.data)
                project.save_project()
                flash('Project created!')
                return redirect(url_for('admin'))
        else:
            del_project = Projects.query.filter_by(name=project_action.name.data).first()
            if del_project:
                portfolio.session.delete(del_project)
                portfolio.session.commit()
                return redirect(url_for('admin'))
            else:
                flash('That project doesnt exist')
                return redirect(url_for('admin'))
            
    if blog_action.validate_on_submit():
        if blog_action.action.data == 'Create':
            search_blog = Blog.query.filter_by(name=blog_action.name.data).first()
            if search_blog:
                flash('A blog with that name already exists!')
                return redirect(url_for('admin'))
            else:
                blog = Blog(name=blog_action.name.data, description=blog_action.description.data, img=blog_action.img.data)
                blog.save_blog()
                flash('Blog Created!')
                return redirect(url_for('admin'))
        else:
            del_blog = Blog.query.filter_by(name=blog_action.name.data).first()
            if del_blog:
                portfolio.session.delete(del_blog)
                portfolio.session.commit()
                flash('Blog Deleted')
                return redirect(url_for('admin'))
            else:
                flash('That blog name doesnt exist')
                return redirect(url_for('admin'))
    
    if email_action.validate_on_submit():
        blog = Blog.query.filter_by(name=email_action.blog.data).first()
        post = Post(subject=email_action.subject.data, content=email_action.body.data, blog=blog)
        post.save_post()
        msg = Message(subject=email_action.subject.data, sender='yisroelbaum8@gmail.com', recipients=[recipient.email for recipient in blog.followers], )
        msg.body = email_action.body.data
        mail.send(msg)
        flash('Email sent!')
        return redirect(url_for('admin'))
        
    all_blogs = Blog.query.all()
    all_projects = Projects.query.all()
    all_messages = MessageToAdmin.query.all()
           
    return render_template('admin_page.html', 
                           blog_action=blog_action, 
                           project_action=project_action, 
                           email_action=email_action,
                           all_blogs=all_blogs, 
                           all_projects=all_projects,
                           all_messages=all_messages
                           )
