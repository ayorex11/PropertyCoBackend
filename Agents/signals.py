
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile when a User is created with account_type 'Agent'
    """
    if created and instance.account_type == 'Agent':
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email_address=instance.email,
            member_id=instance.member_id,
            contact_number = instance.phone_number
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to update the Profile when User is saved (if account_type is 'Agent')
    """
    if instance.account_type == 'Agent' and hasattr(instance, 'profile'):
        instance.profile.first_name = instance.first_name
        instance.profile.last_name = instance.last_name
        instance.profile.email_address = instance.email
        instance.profile.member_id = instance.member_id
        instance.profile.contact_number = instance.phone_number
        instance.profile.save()