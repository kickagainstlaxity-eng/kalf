import re
from flask import Blueprint, flash, redirect, render_template, request, url_for
from email_validator import validate_email, EmailNotValidError

main_bp = Blueprint("main", __name__)

# Basic RFC 5322 compliant email regex
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/donate")
def donate():
    return render_template("donate.html")



@main_bp.route("/thank-you")
def thank_you():
    return render_template("thankyou.html")


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # 1. Extract the form data using the 'name' attributes
        full_name = request.form.get('full-name').strip()
        email = request.form.get('email').strip()
        subject = request.form.get('subject')
        message = request.form.get('message').strip()

        try:
            # Validates syntax and delivers a normalized email address
            email_info = validate_email(email, check_deliverability=True)
            email = email_info.normalized
        except EmailNotValidError as e:
            flash(f"Invalid email address: {str(e)}", "error")
            return redirect(url_for('main.contact'))

        # 2. Basic Server-Side Validation
        if not full_name or not email or not message:
            flash("Please fill out all required fields.", "error")
            return redirect(url_for('main.contact'))

        # 3. Process the data (Example: Send an email, log, or save to DB)
        try:
            # OPTION A: Log to console for debugging
            print(f"New Message from {full_name} ({email})")
            print(f"Subject: {subject}")
            print(f"Message: {message}")

            # OPTION B: (Add your Database save or Flask-Mail logic here)
            # db.session.add(ContactMessage(name=full_name, email=email, ...))
            # db.session.commit()

            # 4. Success feedback and redirect
            flash("Thank you! Your message has been sent successfully.", "success")
            return redirect(url_for('main.contact'))

        except Exception as e:
            # Handle unexpected processing errors
            print(f"Error processing contact form: {e}")
            flash("An error occurred while sending your message. Please try again.", "error")
            return redirect(url_for('main.contact'))

    # If GET request, simply render the template containing your contact form
    return render_template('contact.html')



@main_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip()

    # 1. Fallback URL in case request.referrer is empty
    next_page = request.referrer or url_for('main.index')

    # 2. Check if email was provided
    if not email:
        flash("Email address is required to subscribe.", "error")
        return redirect(next_page)

    # 3. Validate Email Format
    if not re.match(EMAIL_REGEX, email):
        flash("Please enter a valid email address.", "error")
        return redirect(next_page)

    try:
        # 4. Save to DB or send to marketing platform (e.g., Mailchimp, SendGrid)
        print(f"New Newsletter Subscriber: {email}")
        
        # db.session.add(Subscriber(email=email))
        # db.session.commit()

        flash("Thank you for subscribing to our newsletter!", "success")
    except Exception as e:
        print(f"Newsletter Subscription Error: {e}")
        flash("Something went wrong. Please try again later.", "error")

    # 5. Redirect the user back to the exact page they signed up from
    return redirect(next_page)