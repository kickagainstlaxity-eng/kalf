from datetime import datetime
import os
import uuid
from dotenv import load_dotenv
from flask import Blueprint, abort, flash, render_template, redirect, url_for, request
import requests

from services.json_service import load_json_file
from services.program_service import find_program_by_id, find_student_by_id, save_student_to_db

programs_bp = Blueprint("programs", __name__)

load_dotenv()

# Temporary enrollment database file
ENROLLMENTS_FILE = "static/data/enrollments.json"

# Mock In-Memory Databases
PENDING_REGISTRATIONS = {}


@programs_bp.route("/programs")
def programs():
    raw_programs = load_json_file("static/data/programs.json")
    raw_events = load_json_file("static/data/events.json")

    # Flatten categories for simplified list rendering
    programs_list = []
    for category, items in raw_programs.items():
        for item in items:
            item["category"] = category
            programs_list.append(item)

    # Process Events into Upcoming & Past dynamically
    upcoming_events = []
    past_events = []
    today = datetime.now().date()

    all_raw_events = raw_events.get("upcoming", []) + raw_events.get("past", [])

    for event in all_raw_events:
        try:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            event["day"] = event_date.strftime("%d")
            event["month_year"] = event_date.strftime("%b %Y").upper()

            if event_date >= today:
                upcoming_events.append(event)
            else:
                past_events.append(event)
        except (ValueError, KeyError) as e:
            print(f"Skipping malformed event: {event}. Error: {e}")

    upcoming_events.sort(key=lambda x: x["date"])
    past_events.sort(key=lambda x: x["date"], reverse=True)

    return render_template(
        "programs.html",
        programs=programs_list,
        upcoming_events=upcoming_events,
        past_events=past_events,
    )


@programs_bp.route("/programs/<program_id>")
def program_detail(program_id):
    active_program, category = find_program_by_id(program_id)

    if not active_program:
        abort(404)

    details = active_program.get("details", {})

    # --- Fetch Recommended Programs ---
    raw_programs = load_json_file("static/data/programs.json")
    all_programs = []
    for cat, items in raw_programs.items():
        for item in items:
            item["category"] = cat
            all_programs.append(item)

    recommended = [p for p in all_programs if p.get("id") != program_id]
    recommended_programs = recommended[:3]

    return render_template(
        "program_list.html",
        program=active_program,
        program_type=category,
        details=details,
        recommended_programs=recommended_programs,
    )


@programs_bp.route("/programs/<program_id>/enroll", methods=["POST"])
def enroll_program(program_id):
    active_program, category = find_program_by_id(program_id)
    if not active_program:
        abort(404)

    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()

    if not full_name or not email:
        flash("Please provide both your name and email.", "error")
        return redirect(url_for("programs.program_detail", program_id=program_id))

    details = active_program.get("details", {})
    investment = None
    for stat in details.get("stats", []):
        label = stat.get("label", "").lower()
        if "investment" in label or "cost" in label or "fee" in label:
            investment = stat.get("value")

    is_free = (
        (not investment)
        or investment.strip().lower() == "free"
        or investment.strip() == "₦0"
    )

    reg_id = str(uuid.uuid4())
    registration = {
        "id": reg_id,
        "program_id": program_id,
        "program_title": active_program.get("title"),
        "full_name": full_name,
        "email": email,
        "amount": "Free" if is_free else investment,
        "created_at": datetime.now().isoformat(),
        "status": "free" if is_free else "pending"
    }

    if is_free:
        # PERSIST IMMEDIATELY: Save free student straight to the file database
        save_student_to_db(registration)
        return redirect(url_for("programs.thank_you", reg_id=reg_id))

    # For paid: stage in pending checkout dictionary
    PENDING_REGISTRATIONS[reg_id] = registration

    try:
        amount_naira = int("".join(ch for ch in investment if ch.isdigit()))
        amount_kobo = amount_naira * 100
    except ValueError:
        flash("Invalid program fee configuration.", "error")
        return redirect(url_for("programs.program_detail", program_id=program_id))

    try:
        resp = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers={"Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"},
            json={
                "email": email,
                "amount": amount_kobo,
                "reference": reg_id,
                "callback_url": url_for("programs.thank_you", _external=True),
                "metadata": {"program_id": program_id, "full_name": full_name},
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        return redirect(data["data"]["authorization_url"])
    except Exception as e:
        print(f"Paystack init failed: {e}")
        flash("Payment initialization failed. Please try again shortly.", "error")
        return redirect(url_for("programs.program_detail", program_id=program_id))

        
@programs_bp.route("/programs/thank-you")
def thank_you():
    reference = request.args.get("reference") or request.args.get("trxref")
    reg_id = request.args.get("reg_id")  # Direct from free registration redirect

    # Scenario A: Free Registration (Lookup from persistent DB)
    if reg_id:
        reg_info = find_student_by_id(reg_id)
        if reg_info:
            return render_template("thank_you.html", registration=reg_info)

    # Scenario B: Paid Registration Callback Verification
    if reference:
        try:
            resp = requests.get(
                f"https://api.paystack.co/transaction/verify/{reference}",
                headers={"Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"},
                timeout=10
            )
            resp_data = resp.json()
            
            if resp.status_code == 200 and resp_data.get("status") and resp_data["data"]["status"] == "success":
                # Check staging cache first
                pending_reg = PENDING_REGISTRATIONS.pop(reference, None)
                
                if pending_reg:
                    pending_reg["status"] = "paid"
                    pending_reg["paystack_ref"] = reference
                    # PERSIST TO FILE DATABASE
                    save_student_to_db(pending_reg)
                    return render_template("thank_you.html", registration=pending_reg)
                
                # If they reload page, check database directly
                already_paid = find_student_by_id(reference)
                if already_paid:
                    return render_template("thank_you.html", registration=already_paid)

        except Exception as e:
            print(f"Paystack verification failed: {e}")

    flash("We could not confirm your enrollment payment. Please contact support.", "error")
    return redirect(url_for("programs.programs"))