
from flask import Blueprint, redirect, render_template


admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/admin/login2020')
def admin_login():
    return render_template("admin_login.html")

@admin_bp.route('/admin/logout')
def admin_logout():
    return redirect("/")

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")

@admin_bp.route('/admin/blog-manager')
def blog_manager():
    return render_template("adminBlog_manager.html")

@admin_bp.route('/admin/program-manager')
def program_manager():
    return render_template("adminProgram_manager.html")

@admin_bp.route('/admin/events-manager')
def event_manager():
    return render_template("adminEvents_manager.html")

@admin_bp.route('/admin/volunteer-list')
def volunteer_list():
    return render_template("adminVolunteer_list.html")

@admin_bp.route('/admin/settings')
def admin_settings():
    return render_template("admin_settings.html")