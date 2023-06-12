from .models import User
from rest_framework import serializers
import re
from .constants import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']

class UpdateSerializer(serializers.ModelSerializer):
    def validate_phone_number(self,data):
        pattern = r"\+?91[\d]{10}"
        if not re.search(pattern,data):
            raise serializers.ValidationError("Phone number should be of the form +91XXXXXXXXXX")
        return data
    class Meta:
        model = User
        fields = ['first_name','last_name','bio','email','profile_picture','phone_number']

class DisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','bio','profile_picture','phone_number']