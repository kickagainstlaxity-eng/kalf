


# --- Blog Routes ---
from datetime import datetime

from flask import Blueprint, render_template

from services.json_service import load_json_file


blog_bp = Blueprint("blog", __name__)

@blog_bp.route('/blog')
def blog():
    posts = load_json_file('static/data/blog.json')
    active_posts = []
    
    for post in posts:
        if post.get('status') is True:
            try:
                date_obj = datetime.strptime(post['created_at'].split('T')[0], '%Y-%m-%d')
                post['formatted_date'] = date_obj.strftime('%B %d, %Y')
            except Exception:
                post['formatted_date'] = "Recent"
            
            raw_content = post.get('content', '')
            post['excerpt'] = raw_content.replace('<p>', '').replace('</p>', '')[:120] + "..."
            active_posts.append(post)

    active_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return render_template('blog.html', posts=active_posts)

@blog_bp.route('/blog/<blog_id>')
def blog_post_detail(blog_id):
    posts = load_json_file('static/data/blog.json')
    post = next((p for p in posts if str(p.get('id')) == str(blog_id) and p.get('status') is True), None)
    if not post:
        abort(404)

    try:
        date_obj = datetime.strptime(post['created_at'].split('T')[0], '%Y-%m-%d')
        post['formatted_date'] = date_obj.strftime('%B %d, %Y')
    except Exception:
        post['formatted_date'] = "Recent"

    related_posts = [p for p in posts if str(p.get('id')) != str(blog_id) and p.get('status') is True][:3]
    for rel in related_posts:
        try:
            date_obj = datetime.strptime(rel['created_at'].split('T')[0], '%Y-%m-%d')
            rel['formatted_date'] = date_obj.strftime('%B %d, %Y')
        except Exception:
            rel['formatted_date'] = "Recent"
        rel['excerpt'] = rel.get('content', '').replace('<p>', '').replace('</p>', '')[:100] + "..."

    return render_template('blog_post.html', post=post, related_posts=related_posts)

