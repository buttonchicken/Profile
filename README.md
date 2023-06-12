# Profile
A django based project which lets a user Register,Login and Update their profile details.

Steps to set up the project:

1. Create a virtual environment and install the necessary dependencies using:
        **pip3 install -r requirements.txt**

2. Make migrations using the command:
        **python3 manage.py makemigrations**

3. Migrate using:
        **python3 manage.py migrate**

Start server using the command:
        **python3 manage.py runserver**

Run the unit tests using the command:
        **python3 manage.py test Accounts**

**Note - JWT Authentication is required for Update API, please generate the access token using login/register api
       and use with every update request**

Postman collection attached in repository for reference
