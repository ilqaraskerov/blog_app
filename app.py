from flask import Flask, render_template, request, redirect

app = Flask(__name__)

posts = []

def get_all_posts():
    return posts

def get_post_by_id(post_id):
    for post in posts:
        if post['id'] == post_id:
            return post
    return None

def add_post(title, content):
    post_id = len(posts) + 1
    post = {'id': post_id, 'title': title, 'content': content}
    posts.append(post)

def update_post(post_id, title, content):
    for post in posts:
        if post['id'] == post_id:
            post['title'] = title
            post['content'] = content
            return True
    return False

def delete_post(post_id):
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            del posts[index]
            return True
    return False

@app.route('/')
def index():
    all_posts = get_all_posts()
    return render_template('index.html', posts=all_posts)

@app.route('/post/<int:post_id>' , methods=['GET', 'POST'])
def post(post_id):
    post = get_post_by_id(post_id)
    if post:
        return render_template('post.html', post=post)
    else:
        return "Post not found", 404

@app.route('/add_post', methods=['GET', 'POST'])
def add_new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        add_post(title, content)
        return redirect('/')
    return render_template('add_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_new_post(post_id):
    post = get_post_by_id(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if update_post(post_id, title, content):
            return redirect('/')
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_new_post(post_id):
    if delete_post(post_id):
        return redirect('/')
    else:
        return "Post not found", 404

if __name__ == '__main__':
    app.run(debug=True)
