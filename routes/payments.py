from flask import Blueprint, request, redirect, url_for, flash
# Adjust your import paths according to your project structure:
from services.paystack import PaystackService

payments_bp = Blueprint('payments', __name__)
paystack_service = PaystackService()

@payments_bp.route('/donate/initialize', methods=['POST'])
def initiate_donation():
    # 1. Parse submitted form parameters
    amount = request.form.get('amount')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone', '')
    note = request.form.get('note', '')

    # Simple validation check
    if not email or not amount:
        flash("Required donor details are missing.", "error")
        return redirect(url_for('main.donate')) # Assuming 'main.donate' is your donate page route

    # 2. Package metadata for custom dashboard displays
    metadata = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "note": note
    }

    # Callback URL: Where Paystack should redirect the user after authorization/payments.
    callback_url = url_for('payments.verify_donation', _external=True)

    # 3. Call Paystack API
    paystack_data = paystack_service.initialize_transaction(
        email=email,
        amount_in_naira=amount,
        callback_url=callback_url,
        metadata=metadata
    )

    if paystack_data and 'authorization_url' in paystack_data:
        # Redirect user immediately to Paystack's secure checkout page
        return redirect(paystack_data['authorization_url'])
    
    # Handle failure gracefully
    flash("Unable to reach the payment gateway. Please try again.", "error")
    return redirect(url_for('main.donate'))


@payments_bp.route('/donate/callback')
def verify_donation():
    # Paystack returns the transaction reference in the query params
    reference = request.args.get('reference') or request.args.get('trxref')

    if not reference:
        flash("Invalid transaction reference received.", "error")
        return redirect(url_for('main.donate'))

    # Call Paystack to verify if payment is legitimately successful
    transaction_data = paystack_service.verify_transaction(reference)

    if transaction_data and transaction_data.get('status') == 'success':
        # Retrieve amount from Paystack response (convert back from Kobo to Naira)
        amount_paid = transaction_data.get('amount') / 100
        
        # Pull metadata for further processing (e.g. adding to Database)
        metadata = transaction_data.get('metadata', {})
        first_name = metadata.get('first_name', '')
        last_name = metadata.get('last_name', '')

        # SUCCESS STAGE: 
        # Here is where you write code to save the donor in your database
        # e.g., db.session.add(Donation(name=f"{first_name} {last_name}", amount=amount_paid, status="completed"))
        # db.session.commit()

        flash(f"Thank you, {first_name} {last_name}! Your donation of ₦{amount_paid:,.2f} was successful.", "success")
        
        # Your HTML's "window.onload" script automatically handles Step 4 (Success Screen)
        # when it finds ?reference=... in the URL query string.
        # So we simply redirect back to the donate page, appending the reference!
        return redirect(url_for('main.donate', reference=reference))

    flash("Payment verification failed. If you were debited, please contact support.", "error")
    return redirect(url_for('main.donate'))