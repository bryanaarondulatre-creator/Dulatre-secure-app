import unittest
import json
from app.main import app, validate_email

class TestEmailValidator(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_validate_email_valid(self):
        """Test valid email addresses"""
        valid_emails = [
            'user@example.com',
            'first.last@example.co.uk',
            'user+tag@example.org',
            '123@example.com'
        ]
        
        for email in valid_emails:
            self.assertTrue(validate_email(email), f"{email} should be valid")
    
    def test_validate_email_invalid(self):
        """Test invalid email addresses"""
        invalid_emails = [
            'invalid',
            'user@',
            '@example.com',
            'user@.com',
            'user@example.'
        ]
        
        for email in invalid_emails:
            self.assertFalse(validate_email(email), f"{email} should be invalid")
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_validate_email_endpoint_valid(self):
        """Test email validation endpoint with valid email"""
        response = self.app.post('/validate-email',
                                json={'email': 'user@example.com'},
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['is_valid'])
    
    def test_validate_email_endpoint_missing_email(self):
        """Test email validation endpoint with missing email"""
        response = self.app.post('/validate-email',
                                json={},
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
