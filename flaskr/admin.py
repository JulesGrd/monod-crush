from flask import Blueprint, render_template

from flaskr.db import get_db


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route('/')
def panel():
    """Show admin panel"""

    db = get_db()
    users = db.execute("SELECT COUNT(id) FROM user").fetchone()
    posts = db.execute("SELECT COUNT(id) FROM post").fetchone()

    return render_template("/admin/panel.html", posts=tuple(posts)[0], users=tuple(users)[0])

#@bp.route("/post/<int:post_id>/-", methods=("POST",))
#@login_required
#def report(post_id: int):
#    """report a post.
#
#    if this post was report 3 times he are hidden while admin check the message
#    """
#    get_post(post_id)
#    report_nb = db.execute("SELECT hidden FROM post WHERE id = ?", post_id)
#    db.execute("UPDATE hidden FROM post SET hidden = ? WHEREid = ?", report_nb +1, post_id ) #add 1 to hidden
#    if report_nb > 2: #hidden message where hidden >= 3
#        
#        
#    return redirect(url_for("blog.index"))