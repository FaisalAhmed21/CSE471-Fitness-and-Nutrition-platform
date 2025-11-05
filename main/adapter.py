from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import Client
import logging

logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle social account sign-in/sign-up
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        # If the user is signing up (not connecting to existing account)
        if sociallogin.is_existing:
            return
        
        # Check if user already exists
        if sociallogin.user.id:
            return
    
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login user.
        """
        try:
            user = super().save_user(request, sociallogin, form)
            
            # Ensure Client record exists
            if not Client.objects.filter(user=user).exists():
                Client.objects.create(
                    user=user,
                    client_usrname=user.username,
                    email=user.email,
                    first_name=user.first_name or "",
                    last_name=user.last_name or ""
                )
            
            return user
        except Exception as e:
            logger.error(f"Error saving user from social login: {e}")
            raise
    
    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to populate user instance from social provider info.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Set default username if not provided
        if not user.username:
            email = data.get('email', '')
            if email:
                base_username = email.split('@')[0]
                # Ensure username is unique
                username = base_username
                counter = 1
                from django.contrib.auth.models import User
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                user.username = username
            else:
                # Fallback to a generated username
                user.username = f"user_{sociallogin.account.uid}"
        
        return user
    
    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """
        Handle authentication errors gracefully
        """
        logger.error(f"Social auth error for {provider_id}: {error} - {exception}")
        
        # Add user-friendly message
        if 'state' in str(error).lower() or 'state' in str(exception).lower():
            messages.error(
                request, 
                'Your login session expired. Please try signing in with Google again.'
            )
        else:
            messages.error(
                request,
                'There was an error signing in with Google. Please try again or use a different method.'
            )
        
        # Redirect to login page instead of showing error page
        raise ImmediateHttpResponse(redirect('clientLogin'))
