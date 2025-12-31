from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_save, post_save, pre_delete, post_delete
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from events.models import Events,RSVP
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=RSVP)
def rsvp_created(sender, instance, created, **kwargs):
    if created:
        print(f"{instance.user.username} RSVP'd as {instance.status} for {instance.event.name}")
            
@receiver(post_save,sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        
        subject = "Activate Your Account"
        message = f"Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank you!"
        recipient_list = [instance.email]
        
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email} : {str(e)}")
        

@receiver(post_save,sender=User)
def assign_role(sender, instance,created, **kwargs):
    if created:
        participants_group,created = Group.objects.get_or_create(name='Participant')
        instance.groups.add(participants_group)
        instance.save()