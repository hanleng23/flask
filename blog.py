class Blog:
    def __init__(self, id, title, text):
        self.id = id
        self.title = title
        self.text = text


from blog import Blog
from flask import Flask, render_template

app = Flask(__name__)

blogs = []
b1 = Blog(1, 'hello1','zhangsan')
b2 = Blog(2, 'hello2','lisi')
blogs.append(b1)
blogs.append(b2)

@app.route('/')
def home ():
    return render_template('home.html')

@app.route('/blogs')
def list_notes():
    return render_template('list_blogs.html',blogs = blogs)

@app.route('/blog/<id>')
def query_blog(id):
    blog = None
    for blg in blogs:
        if blg.id == int(id):
            blog = blg
    return render_template('query_blog.html',blog = blog)
