from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")

@main_bp.route("/donate")
def donate():
    return render_template("donate.html")

@main_bp.route("/thank-you")
def thank_you():
    return render_template("thankyou.html")