from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from .models import Client

@receiver(user_signed_up)
def create_client_for_new_user(request, user, **kwargs):
    """
    Create Client record when a new user signs up (via form or Google)
    """
    if not Client.objects.filter(user=user).exists():
        # Create the Client instance
        Client.objects.create(
            user=user,
            client_usrname=user.username,
            email=user.email,
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )


@receiver(pre_social_login)
def link_to_existing_user(sender, request, sociallogin, **kwargs):
    """
    Ensure Client record exists for social login users
    """
    if sociallogin.is_existing:
        # User already exists, make sure they have a Client record
        user = sociallogin.user
        if user and not Client.objects.filter(user=user).exists():
            Client.objects.create(
                user=user,
                client_usrname=user.username,
                email=user.email,
                first_name=user.first_name or "",
                last_name=user.last_name or ""
            )

