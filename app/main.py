from flask import Flask, jsonify, request
import re

app = Flask(__name__)

def validate_email(email):
    """Secure email validation with proper regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'}), 200

@app.route('/validate-email', methods=['POST'])
def validate_email_endpoint():
    """Email validation endpoint with proper input validation"""
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'error': 'Email field required'}), 400
    
    email = data['email']
    
    if not isinstance(email, str) or len(email) > 254:
        return jsonify({'error': 'Invalid email format'}), 400
    
    is_valid = validate_email(email)
    
    return jsonify({
        'email': email,
        'is_valid': is_valid
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
