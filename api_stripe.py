import stripe
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json

        customer_id = data['customer_id']
        product_name = data['product_name']
        unit_amount = data['unit_amount']  # em centavos
        quantity = data['quantity']
        success_url = data['success_url']
        cancel_url = data['cancel_url']

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            customer=customer_id,
            line_items=[
                {
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': unit_amount,
                    },
                    'quantity': quantity,
                },
            ],
            payment_intent_data={
                'setup_future_usage': 'off_session'
            },
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return jsonify({'checkout_url': session.url})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/')
def home():
    return 'API está rodando com sucesso! 🚀'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
