from flask import Blueprint, render_template, redirect, url_for, request, session

from database import db
from structures import Article, ArticleVisit
from routes.auth import admin_required
from utils import validate_request_item, redirect_with_error, set_error, attempt_form_item

lessons = Blueprint("lessons", __name__)

@lessons.route("/")
def lessons_index():
    return render_template("lessons/index.html.j2", lessons=db.get_all_articles())

@lessons.route("/<int:lesson_id>")
def lesson_detail(lesson_id):
    lesson = db.get_article_by_id(lesson_id)

    if not lesson:
        return redirect(url_for("lessons.lessons_index"))
    
    if "user" in session:
        visit = ArticleVisit(0, session["user"]["id"], lesson_id)
        
        db.log_article_visit(visit)

    lessons = db.get_all_articles()
    lessons.pop(lessons.index(lesson))

    return render_template("lessons/lesson.html.j2", lesson=lesson, lessons=lessons[:5], views=len(db.get_all_article_visits_on_article(lesson_id)))

@lessons.route("/delete/<int:lesson_id>")
@admin_required
def lesson_delete(lesson_id):
    lesson = db.get_article_by_id(lesson_id)

    if not lesson:
        return redirect(url_for("lessons.lessons_index"))

    db.delete_article(lesson.id)

    return redirect(url_for("lessons.lessons_index"))

@lessons.route("/edit/<int:lesson_id>", methods=["GET", "POST"])
@admin_required
def lesson_edit(lesson_id):
    lesson = db.get_article_by_id(lesson_id)

    if not lesson and not lesson_id == 0:
        return redirect(url_for("lessons.lessons_index"))

    if lesson_id == 0:
        lesson = Article(0, "New Lesson", "", "")

    if request.method == "POST":
        if not validate_request_item("title") or not validate_request_item("body") or not validate_request_item("tags"):
            set_error("Missing parameters, try again")
            
            # pass through any of the title, body and tags that we can so nothing is lost if something is forgotten when clicking submit.
            lesson.title = attempt_form_item("title") or lesson.title
            lesson.body = attempt_form_item("body") or lesson.body
            lesson.tags = attempt_form_item("tags") or lesson.tags
            
            return render_template("lessons/admin/edit.html.j2", lesson=lesson)

        lesson.title = request.form["title"]
        lesson.body = request.form["body"]
        lesson.tags = request.form["tags"]

        if lesson_id == 0:
            db.create_article(lesson)
        else:
            db.update_article(lesson)

        return redirect(url_for("lessons.lesson_detail", lesson_id=lesson_id))

    return render_template("lessons/admin/edit.html.j2", lesson=lesson)
