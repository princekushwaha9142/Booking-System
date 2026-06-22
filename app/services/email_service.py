import logging
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)


async def send_email(to_email: str, subject: str, body: str):
    """Abhi logs mein print karta hai. Production mein SMTP se replace karo."""
    logger.info("=" * 50)
    logger.info("📧 EMAIL NOTIFICATION")
    logger.info("To:      %s", to_email)
    logger.info("Subject: %s", subject)
    logger.info("Body:\n%s", body.strip())
    logger.info("=" * 50)


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