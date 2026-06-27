import logging
from app.core.celery_app import celery_app
from app.core.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name="tasks.send_email",
)
def send_email_task(self, to_email: str, subject: str, body: str):
    """
    Celery task to send email via Resend.
    Retries up to 3 times on failure with 60s delay.
    """
    try:
        if settings.RESEND_API_KEY:
            import resend
            resend.api_key = settings.RESEND_API_KEY
            params: resend.Emails.SendParams = {
                "from": settings.FROM_EMAIL,
                "to": [to_email],
                "subject": subject,
                "text": body,
            }
            resend.Emails.send(params)
            logger.info("✅ Email sent to %s | Subject: %s", to_email, subject)
        else:
            logger.info("📧 EMAIL (no API key) | To: %s | Subject: %s", to_email, subject)

    except Exception as exc:
        logger.error("❌ Email failed: %s — retrying...", exc)
        raise self.retry(exc=exc)