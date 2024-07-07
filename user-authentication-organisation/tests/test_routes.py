#!/usr/bin/env/ python3
"""
Module supplies tests cases for out api routes
"""
import unittest
from api.views import create_app, db
from models.user import User
import json
from models.organisation import Organisation


class RoutesTestCase(unittest.TestCase):
    """
    Defines test cases for our routes
    """
    registration_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123"
        }

    def setUp(self) -> None:
        """
        Set up the test environment
        """
        self.app = create_app('test')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        """
        Tear down the test environment
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        """
        Tests user registration with default organisation
        """
        response = self.client.post(
            '/auth/register',
            data=json.dumps(self.registration_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Registration successful')
        self.assertIn('accessToken', response_data['data'])

        user = User.query.filter_by(email='john.doe@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.firstName, 'John')
        self.assertEqual(user.lastName, 'Doe')

        org = Organisation.query.filter(
            Organisation.users.any(email='john.doe@example.com')
            ).first()
        self.assertIsNotNone(org)
        self.assertEqual(org.name, "John's Organisation")

    def test_user_login_success(self):
        """
        Tests login is done successfully
        """
        self.client.post(
            '/auth/register',
            data=json.dumps(self.registration_data),
            content_type='application/json'
        )
        login_data = {
            "email": self.registration_data["email"],
            "password": self.registration_data["password"]
        }
        response = self.client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Login successful')
        self.assertIn('accessToken', response_data['data'])
        self.assertEqual(
            response_data['data']['user']['email'],
            self.registration_data["email"]
            )

    def test_login_failure_invalid_email(self):
        """
        Tests that login fails with invalid email
        """
        self.client.post(
            '/auth/register',
            data=json.dumps(self.registration_data),
            content_type='application/json'
        )
        login_data = {
            "email": "invalid.email@example.com",
            "password": self.registration_data["password"]
        }
        response = self.client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Bad request')
        self.assertEqual(response_data['message'], 'Authentication failed')

    def test_login_failure_invalid_password(self):
        """
        Tests that login fails with invalid password
        """
        self.client.post(
            '/auth/register',
            data=json.dumps(self.registration_data),
            content_type='application/json'
        )
        login_data = {
            "email": self.registration_data["email"],
            "password": "wrongpassword"
        }
        response = self.client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Bad request')
        self.assertEqual(response_data['message'], 'Authentication failed')

    def test_login_failure_missing_fields(self):
        """
        Test that login fails with missing fields
        """
        self.client.post(
            '/auth/register',
            data=json.dumps(self.registration_data),
            content_type='application/json'
            )
        login_data = {
            "email": self.registration_data["email"]
        }
        response = self.client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Bad request')
        self.assertEqual(response_data['message'], 'Authentication failed')

    def test_register_missing_firstName(self):
        """
        Test that registration fails when firstName is missing
        """
        data = {
            "lastName": "Doe",
            "email": "missing.firstname@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 422)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['errors'][0]['field'], 'firstName')
        self.assertEqual(
            response_data['errors'][0]['message'],
            'firstName Missing'
            )

    def test_register_missing_lastName(self):
        """
        Test that registration fails when lastName is missing
        """
        data = {
            "firstName": "John",
            "email": "missing.lastname@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 422)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['errors'][0]['field'], 'lastName')
        self.assertEqual(
            response_data['errors'][0]['message'],
            'lastName Missing'
            )

    def test_register_missing_email(self):
        """
        Test that registration fails when email is missing
        """
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(
            '/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 422)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['errors'][0]['field'], 'email')
        self.assertEqual(
            response_data['errors'][0]['message'],
            'email Missing'
            )

    def test_register_duplicate_userID(self):
        """
        Test that registration fails when UserID already exists
        """
        response = self.client.post(
            '/auth/register',
            data=json.dumps(self.registration_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            '/auth/register',
            data=json.dumps(self.registration_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'Bad request')
        self.assertEqual(response_data['message'], 'Registration unsuccessful')


if __name__ == '__main__':
    unittest.main()
