from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

def upload_to(instance, filename):
    return '{username}/{filename}'.format(username = instance.username,filename=filename)

class User(AbstractUser):
    phone_number = models.CharField(max_length=13, null=True, unique=True)
    bio = models.CharField(max_length=256)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def get_image_url(self):
        return request.build_absolute_uri(self.url)
