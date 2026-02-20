from rest_framework import serializers
from .models import Book,Loan,Author,LoanRequest,Transaction,User
from django.contrib.auth import authenticate
from .utils import get_tokens_for_user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'
        read_only_fields=['ISBN','available_copies']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Loan
        fields='__all__'
        read_only_fields=['loan_id','loan_date']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanRequest
        fields='__all__'
        read_only_fields=['member','book']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'
        read_only_fields=['created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','role']
    
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    tokens=serializers.SerializerMethodField(read_only=True)
    role=serializers.CharField(read_only=True)
    
    def validate(self,attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        

        if username and password:
            user=authenticate(username=username,password=password)
            if user is None:
                raise serializers.ValidationError("Invalid Credentials")
            
            attrs['user']=user
            attrs['tokens']=get_tokens_for_user(user)
            attrs['role']=user.role
            return attrs
        
        else:
            raise serializers.ValidationError("Username and Password are required")