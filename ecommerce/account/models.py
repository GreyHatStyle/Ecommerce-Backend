import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class AddressTypeChoices(models.TextChoices):
    HOME = "Home"
    WORK = "Work"
    OTHER = "Other"

class User(AbstractUser):
     # Reference: https://tomharrisonjr.com/uuid-or-guid-as-primary-keys-be-careful-7b2aa3dcb439
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone_no = PhoneNumberField(null=False, blank=False, unique=True)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        "phone_no",
    ]
    
    class Meta:
        db_table = "Users"


class UserAddress(models.Model):
    """
    Since user may have different addresses to deliver products.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    
    # Assuming international users
    pincode = models.CharField(max_length=32, null=False, blank=False)
    
    address_type = models.CharField(
        max_length=20, 
        choices=AddressTypeChoices.choices, 
        default=AddressTypeChoices.HOME,
    )
    
    main_address = models.CharField(max_length=300, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    state = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=30, null=False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.user.username} -> {self.address_type} -> {self.main_address[:20]}"
    
    class Meta:
        db_table = "UserAddress"