import logging
from fastapi import BackgroundTasks
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_email(to_email: str, subject: str, body: str):
    if settings.RESEND_API_KEY:
        try:
            import resend
            resend.api_key = settings.RESEND_API_KEY
            params: resend.Emails.SendParams = {
                "from": settings.FROM_EMAIL,
                "to": [to_email],
                "subject": subject,
                "text": body,
            }
            resend.Emails.send(params)
            logger.info("✅ Email sent to %s", to_email)
        except Exception as e:
            logger.error("❌ Email failed: %s", e)
    else:
        logger.info("📧 EMAIL | To: %s | Subject: %s", to_email, subject)


def notify_booking_confirmed(
    background_tasks: BackgroundTasks,
    email: str, name: str, reference: str, title: str,
):
    body = f"Hi {name},\n\nBooking CONFIRMED!\nReference: {reference}\n{title}\n\nThanks,\nBookingSystem"
    background_tasks.add_task(send_email, email, f"Booking Confirmed — {reference}", body)


def notify_booking_cancelled(
    background_tasks: BackgroundTasks,
    email: str, name: str, reference: str, title: str,
):
    body = f"Hi {name},\n\nBooking CANCELLED.\nReference: {reference}\n{title}\n\nBookingSystem"
    background_tasks.add_task(send_email, email, f"Booking Cancelled — {reference}", body)


def notify_task_created(
    background_tasks: BackgroundTasks,
    email: str, name: str, task_title: str,
):
    body = f"Hi {name},\n\nNew task created: {task_title}\n\nBookingSystem"
    background_tasks.add_task(send_email, email, "New Task Created", body)