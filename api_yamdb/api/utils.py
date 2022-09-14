from django.core.mail import send_mail


def send_confirmation_email(token, email):
    """Send email with confirmation code."""
    subject = "YamDB email confirmation token"
    message = f"""
    Confirmation code: {token}
    """
    from_email = "norelay@yamdb.test"
    send_mail(subject, message, from_email, [email])
