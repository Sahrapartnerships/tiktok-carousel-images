from flask import Flask, request, jsonify
import stripe
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_...')
endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_...')
PDF_DOWNLOAD_URL = os.environ.get('PDF_URL', 'https://storage.yourdomain.com/elternratgeber.pdf')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    
    # Handle successful payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Check if it's our product
        metadata = session.get('metadata', {})
        if metadata.get('product_id') != 'elternratgeber_19':
            return jsonify({'status': 'ignored'}), 200
        
        # Get customer details
        customer_email = session['customer_details']['email']
        customer_name = session['customer_details'].get('name', 'Kunde')
        
        # Log the sale
        print(f"[{datetime.now()}] SALE: {customer_email} - 19€")
        
        # TODO: Send email with download link
        # For now, just log it
        # Integrate with Resend/SendGrid/AWS SES here
        
        return jsonify({
            'status': 'success',
            'email': customer_email,
            'amount': '19.00 EUR'
        }), 200
    
    return jsonify({'status': 'received'}), 200

@app.route('/')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'Elternratgeber Stripe Webhook',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4242, debug=True)
