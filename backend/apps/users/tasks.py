from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mass_mail

from backend import celery_app as app

User = get_user_model()


@app.task(bind=True, default_retry_delay=5 * 60)
def send_spam_emails(self):
    """
    Sends spam emails to all users with is_spam_email=True and is_active=True.
    Retries in case of failure.
    """
    try:
        # Get all users who are marked as spam and active
        spam_users = User.objects.filter(is_spam_email=True, is_active=True)

        # If no spam users found, return a message indicating so
        if not spam_users.exists():
            return "No spam users found"

        # Set up email details
        subject = "Test spam mass email with celery"
        message = "Testing"
        from_email = settings.EMAIL_HOST_USER

        # Create a list of email messages
        email_messages = [(subject, message, from_email, [user.email]) for user in spam_users]

        # Send the emails
        send_mass_mail(email_messages, fail_silently=True)

        return "Emails sent successfully"
    except Exception as exc:
        # If an exception occurs, retry the task after 60 seconds
        raise self.retry(exc=exc, countdown=60)
