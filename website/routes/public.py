from flask import Blueprint, render_template
from database import db

public = Blueprint("public", __name__)

@public.route("/")
def index():
    return render_template(
        "index.html.j2",
        articles = db.get_all_articles()[:5]
    )