from celery import shared_task  # Import Celery shared_task decorator for creating asynchronous tasks
from django.core.mail import send_mail  # Import send_mail function to send emails
from django.template.loader import render_to_string  # Import to render HTML templates to strings
from django.conf import settings  # Import settings for accessing Django settings
from django.utils.html import strip_tags  # Import to strip HTML tags from messages

@shared_task
def send_verification_email(mail_subject, html_message, recipient_list):
    """
    Asynchronous task to send account verification email.

    Args:
        mail_subject (str): Subject line for the email.
        html_message (str): HTML content of the email.
        recipient_list (list): List of recipient email addresses.
    """
    plain_message = strip_tags(html_message)  # Convert HTML message to plain text
    send_mail(
        mail_subject,  # Email subject
        plain_message,  # Plain text message
        settings.EMAIL_HOST_USER,  # Sender's email address from settings
        recipient_list,  # List of recipients
        html_message=html_message  # HTML message content
    )

@shared_task
def send_password_reset_email(mail_subject, html_message, recipient_list):
    """
    Asynchronous task to send password reset email.

    Args:
        mail_subject (str): Subject line for the email.
        html_message (str): HTML content of the email.
        recipient_list (list): List of recipient email addresses.
    """
    plain_message = strip_tags(html_message)  # Convert HTML message to plain text
    send_mail(
        mail_subject,  # Email subject
        plain_message,  # Plain text message
        settings.EMAIL_HOST_USER,  # Sender's email address from settings
        recipient_list,  # List of recipients
        html_message=html_message  # HTML message content
    )
