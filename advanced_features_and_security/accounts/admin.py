# advanced_features_and_security/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the CustomUser model.
    """
    
    # Fields to display in the user list view
    list_display = (
        'email', 
        'username', 
        'get_full_name', 
        'age_display',
        'is_active', 
        'is_staff', 
        'date_joined',
        'profile_photo_display'
    )
    
    # Fields that can be used for filtering in the admin
    list_filter = (
        'is_active', 
        'is_staff', 
        'is_superuser', 
        'date_joined', 
        'last_login'
    )
    
    # Fields that can be searched
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    
    # Default ordering
    ordering = ('-date_joined',)
    
    # Fields that are clickable links in the list view
    list_display_links = ('email', 'username')
    
    # Number of items per page
    list_per_page = 25
    
    # Fields to display in the user detail/edit form
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name', 
                'last_name', 
                'date_of_birth', 
                'phone_number', 
                'bio',
                'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            ),
            'classes': ('collapse',)  # Make this section collapsible
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email', 
                'password1', 
                'password2',
                'first_name',
                'last_name',
                'date_of_birth',
                'phone_number',
                'is_active',
                'is_staff'
            ),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')
    
    # Custom methods for display
    def get_full_name(self, obj):
        """Display the user's full name."""
        return obj.get_full_name() or '-'
    get_full_name.short_description = _('Full Name')
    
    def age_display(self, obj):
        """Display the user's age."""
        age = obj.age
        if age is not None:
            return f"{age} years"
        return '-'
    age_display.short_description = _('Age')
    
    def profile_photo_display(self, obj):
        """Display a thumbnail of the profile photo."""
        if obj.profile_photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_photo.url
            )
        return '-'
    profile_photo_display.short_description = _('Photo')
    
    # Custom actions
    def make_active(self, request, queryset):
        """Mark selected users as active."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            f'{updated} user(s) were successfully marked as active.'
        )
    make_active.short_description = _('Mark selected users as active')
    
    def make_inactive(self, request, queryset):
        """Mark selected users as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            f'{updated} user(s) were successfully marked as inactive.'
        )
    make_inactive.short_description = _('Mark selected users as inactive')
    
    # Add custom actions to the admin
    actions = ['make_active', 'make_inactive']
    
    # Custom form validation
    def save_model(self, request, obj, form, change):
        """
        Custom save method to handle additional logic when saving users.
        """
        # Example: Log user creation/updates
        if not change:  # Creating new user
            # You can add custom logic here for new user creation
            pass
        else:  # Updating existing user
            # You can add custom logic here for user updates
            pass
        
        super().save_model(request, obj, form, change)
    
    # Customize the admin interface appearance
    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the form based on the user's permissions.
        """
        form = super().get_form(request, obj, **kwargs)
        
        # If the current user is not a superuser, restrict some fields
        if not request.user.is_superuser:
            # Remove sensitive fields for non-superusers
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].disabled = True
        
        return form
    
    def get_queryset(self, request):
        """
        Optimize queries by selecting related fields.
        """
        return super().get_queryset(request).select_related()