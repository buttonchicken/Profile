from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from PIL import Image
import io

class RegisterTests(APITestCase):
    
    def test_create_account(self):
        '''Testing for the health of Register API'''
        url = reverse('Accounts:Register')
        creds = {'username': 'test1', 'password': 'Test@12345'}
        response = self.client.post(url, creds, format='json') #creating an account with the above credentials
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED) #checking for exceptions in API
        self.assertEqual(User.objects.count(), 1) #checking whether the user object has been created
        self.assertEqual(User.objects.get().username, 'test1') #checking if the field has been mapped correctly
    
    def test_create_duplicate_account(self):
        '''Testing the prevention of redundant data in Register API'''
        url = reverse('Accounts:Register')
        data = {'username': 'test1', 'password': 'tt@12345'}
        self.client.post(url, data, format='json') #creating an account with the above credentials
        response = self.client.post(url, data, format='json') #creating an account with the above credentials once again
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) #checking if API is able to prevent creation of User with same username
    
class LoginTest(APITestCase):

    def test_login(self):
        '''Testing for the health of Login API'''
        creds = {'username': 'test1', 'password': 'Test@12345'}
        self.client.post(reverse('Accounts:Register'), creds, format='json') #creating an account with the above credentials
        url = reverse('Accounts:Login')
        wrong_creds = {'username': 'test1', 'password': 'rest@12345'} #logging in with the above credentials
        response_for_invalid = self.client.post(url, wrong_creds, format='json') #logging in with incorrect credentials
        response_for_valid = self.client.post(url, creds, format='json') #logging in with correct credentials
        self.assertEqual(response_for_invalid.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_for_valid.status_code, status.HTTP_202_ACCEPTED)

class UpdateProfileTest(APITestCase):
     
    def setUp(self) :
        '''Fetching the JWT Token after account creation'''
        creds = {'username': 'test1', 'password': 'Test@12345'}
        self.access_token = self.client.post(reverse('Accounts:Register'), creds, format='json').data.get("access") #creating an account with the above credentials and fetching the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}') #setting the JWT token in the header

    def generate_photo_file(self):
        '''Generating a random photo for testing profile picture'''
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
    
    def generate_text_file(self):
        '''Generating a random text file for testing profile picture'''
        file =  open('textfile.txt', 'w+')
        file.write("this is a random text file")
        return file

    def test_for_email(self):
        '''Testing for email validators'''
        valid_data = {'email': 'aditya@gmail.com'}
        invalid_data = {'email': 'abcd@'}
        response_for_valid = self.client.patch(reverse('Accounts:Update'), valid_data, format='json') #updating an account with a valid email 
        response_for_invalid = self.client.patch(reverse('Accounts:Update'), invalid_data, format='json') #updating an account with invalid email 
        self.assertEqual(response_for_invalid.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_for_valid.status_code, status.HTTP_202_ACCEPTED)
    
    def test_for_phone(self):
        valid_data = {'phone_number': '+918989898989'}
        invalid_data = {'phone_number': '+19898989a921'}
        response_for_valid = self.client.patch(reverse('Accounts:Update'), valid_data, format='json') #updating an account with a valid phone number
        response_for_invalid = self.client.patch(reverse('Accounts:Update'), invalid_data, format='json') #updating an account with a invalid phone number 
        self.assertEqual(response_for_invalid.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_for_valid.status_code, status.HTTP_202_ACCEPTED)
    
    def test_for_profile_picture(self):
        photo_file = self.generate_photo_file()
        text_file = self.generate_text_file()
        valid_data = {'profile_picture': photo_file}
        invalid_data = {'profile_picture': text_file}
        response_for_valid = self.client.patch(reverse('Accounts:Update'), valid_data, format='multipart') #updating an account with valid file type (png)
        response_for_invalid = self.client.patch(reverse('Accounts:Update'), invalid_data, format='multipart') #updating an account with valid file type (txt)
        self.assertEqual(response_for_valid.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response_for_invalid.status_code, status.HTTP_400_BAD_REQUEST)
