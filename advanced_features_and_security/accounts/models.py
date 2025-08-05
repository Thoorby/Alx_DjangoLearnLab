# accounts/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager for our CustomUser model.
    This handles the logic for creating users and superusers.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        # Validate that email is provided
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        # Normalize the email (convert to lowercase, etc.)
        email = self.normalize_email(email)
        
        # Create user instance
        user = self.model(email=email, **extra_fields)
        
        # Set password (this hashes it automatically)
        user.set_password(password)
        
        # Save to database
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        # Set required superuser fields
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Validate superuser fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        # Use create_user method to create the superuser
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    This adds additional fields and changes authentication to use email.
    """
    
    # Override email field to make it unique and required
    email = models.EmailField(
        _('email address'), 
        unique=True,
        help_text=_('Required. Enter a valid email address.')
    )
    
    # Additional custom fields
    date_of_birth = models.DateField(
        _('date of birth'), 
        null=True, 
        blank=True,
        help_text=_('Enter your date of birth (YYYY-MM-DD)')
    )
    
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text=_('Upload a profile photo (optional)')
    )
    
    # Timestamp fields
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # Set email as the field used for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Fields required when creating superuser
    
    # Use our custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the user."""
        return f"{self.email} ({self.get_full_name() or self.username})"
    
    @property
    def age(self):
        """Calculate and return the user's age."""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None