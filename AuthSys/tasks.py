from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

@shared_task
def send_verification_email(mail_subject, html_message, recipient_list):
    plain_message = strip_tags(html_message)
    send_mail(
        mail_subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        html_message=html_message
    )

@shared_task
def send_password_reset_email(mail_subject, html_message, recipient_list):
    plain_message = strip_tags(html_message)
    send_mail(
        mail_subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        html_message=html_message
    )
