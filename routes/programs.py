
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for

from services.json_service import load_json_file
from services.program_service import (
    load_programs,
    get_all_programs,
    find_program_by_id,
    get_recommended,
)


programs_bp = Blueprint("programs", __name__)

@programs_bp.route('/programs')
def programs():
    raw_programs = load_json_file('static/data/programs.json')
    raw_events = load_json_file('static/data/events.json')

    # Flatten categories for simplified list rendering
    programs_list = []
    for category, items in raw_programs.items():
        for item in items:
            item['category'] = category
            programs_list.append(item)

    # Process Events into Upcoming & Past dynamically
    upcoming_events = []
    past_events = []
    today = datetime.now().date()
    
    all_raw_events = raw_events.get('upcoming', []) + raw_events.get('past', [])
    
    for event in all_raw_events:
        try:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
            event['day'] = event_date.strftime('%d')
            event['month_year'] = event_date.strftime('%b %Y').upper()
            
            if event_date >= today:
                upcoming_events.append(event)
            else:
                past_events.append(event)
        except (ValueError, KeyError) as e:
            print(f"Skipping malformed event: {event}. Error: {e}")

    upcoming_events.sort(key=lambda x: x['date'])
    past_events.sort(key=lambda x: x['date'], reverse=True)

    return render_template(
        'programs.html', 
        programs=programs_list, 
        upcoming_events=upcoming_events, 
        past_events=past_events
    )

@programs_bp.route('/programs/<program_id>')
def program_detail(program_id):
    active_program, category = find_program_by_id(program_id)

    if not active_program:
        abort(404)
        
    details = active_program.get('details', {})
    
    # --- Fetch Recommended Programs ---
    # Load all programs to pick alternatives
    raw_programs = load_json_file('static/data/programs.json')
    all_programs = []
    for cat, items in raw_programs.items():
        for item in items:
            item['category'] = cat
            all_programs.append(item)
            
    # Filter out the current active program so you don't recommend the same page
    recommended = [p for p in all_programs if p.get('id') != program_id]
    # Slice the first 3 or 4 alternative options to display at the bottom
    recommended_programs = recommended[:3]
    
    return render_template(
        'program_list.html',
        program=active_program,
        program_type=category,
        details=details,
        recommended_programs=recommended_programs  # <-- Added this variable
    )

@programs_bp.route('/programs/<program_id>/enroll', methods=['POST'])
def enroll_program(program_id):
    active_program, category = find_program_by_id(program_id)
    if not active_program:
        abort(404)

    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()

    if not full_name or not email:
        flash("Please provide both your name and email.")
        return redirect(url_for('program_detail', program_id=program_id))

    # Determine if this program has a fee
    details = active_program.get('details', {})
    investment = None
    for stat in details.get('stats', []):
        label = stat.get('label', '').lower()
        if 'investment' in label or 'cost' in label or 'fee' in label:
            investment = stat.get('value')

    is_free = (not investment) or investment.strip().lower() == 'free' or investment.strip() == '₦0'

    reg_id = str(uuid.uuid4())
    registration = {
        "id": reg_id,
        "program_id": program_id,
        "program_title": active_program.get('title'),
        "full_name": full_name,
        "email": email,
        "amount": investment,
        "created_at": datetime.now().isoformat(),
    }

    if is_free:
        # Free program: register immediately
        PAID_STUDENTS.append(registration)
        return redirect(url_for('thank_you'))

    # Paid program: stash pending registration, kick off Paystack
    PENDING_REGISTRATIONS[reg_id] = registration

    # Convert "₦500" -> integer kobo amount for Paystack
    try:
        amount_naira = int(''.join(ch for ch in investment if ch.isdigit()))
        amount_kobo = amount_naira * 100
    except ValueError:
        flash("Invalid program fee configuration.")
        return redirect(url_for('program_detail', program_id=program_id))

    try:
        resp = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers={"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"},
            json={
                "email": email,
                "amount": amount_kobo,
                "reference": reg_id,
                "callback_url": url_for('thank_you', _external=True),
                "metadata": {"program_id": program_id, "full_name": full_name},
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        authorization_url = data["data"]["authorization_url"]
        return redirect(authorization_url)
    except Exception as e:
        print(f"Paystack init failed: {e}")
        flash("Payment initialization failed. Please try again shortly.")
        return redirect(url_for('program_detail', program_id=program_id))
