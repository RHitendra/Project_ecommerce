from celery import shared_task
from time import sleep
from django.core.mail import send_mail

@shared_task
def emailsender(email_id, message):
    send_mail('For Doing Shopping on Ecommerce Website',message,'hitendrasinh2101@gmail.com',[email_id],fail_silently=False)
    return None
