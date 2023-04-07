from portfolio import portfolio

user_blogs = portfolio.Table('user_blogs',
                              portfolio.Column('user_id', portfolio.Integer, portfolio.ForeignKey('user.id')),
                              portfolio.Column('blog_id', portfolio.Integer, portfolio.ForeignKey('blog.id'))
                              )

class User(portfolio.Model):
    id       = portfolio.Column(portfolio.Integer, primary_key=True)
    name     = portfolio.Column(portfolio.String(64), nullable=False)
    email    = portfolio.Column(portfolio.String(64), nullable=False, unique=True)
    messages = portfolio.relationship('MessageToAdmin', backref='user', lazy='dynamic')
    blogs    = portfolio.relationship('Blog', secondary=user_blogs, backref='followers')

    def save_user(self):
        portfolio.session.add(self)
        portfolio.session.commit()

class MessageToAdmin(portfolio.Model):
    id      = portfolio.Column(portfolio.Integer, primary_key=True)
    text    = portfolio.Column(portfolio.String(64), nullable=False)
    sent_by = portfolio.Column(portfolio.Integer, portfolio.ForeignKey('user.id'))

    def save_message(self):
        portfolio.session.add(self)
        portfolio.session.commit()

class Blog(portfolio.Model):
    id          = portfolio.Column(portfolio.Integer, primary_key=True)
    name        = portfolio.Column(portfolio.String(64), nullable=False)
    description = portfolio.Column(portfolio.String(200), nullable=False)
    img         = portfolio.Column(portfolio.String(200), default='static/default_pic.jpg')
    posts       = portfolio.relationship('Post', backref='blog', lazy='dynamic')

    def save_blog(self):
        portfolio.session.add(self)
        portfolio.session.commit()

class Post(portfolio.Model):
    id           = portfolio.Column(portfolio.Integer, primary_key=True)
    subject      = portfolio.Column(portfolio.String(64), nullable=False)
    content      = portfolio.Column(portfolio.String(2000), nullable=False)
    blog_id = portfolio.Column(portfolio.Integer, portfolio.ForeignKey('blog.id'))

    def save_post(self):
        portfolio.session.add(self)
        portfolio.session.commit()
class Projects(portfolio.Model):
    id          = portfolio.Column(portfolio.Integer, primary_key=True)
    name        = portfolio.Column(portfolio.String(64), nullable=False)
    description = portfolio.Column(portfolio.String(200), nullable=False)
    url         = portfolio.Column(portfolio.String(64), nullable=False)

    def save_project(self):
        portfolio.session.add(self)
        portfolio.session.commit()