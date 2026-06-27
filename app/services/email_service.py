import logging
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)


def _send_via_celery(to_email: str, subject: str, body: str):
    """Send email via Celery task queue."""
    from app.tasks.email_tasks import send_email_task
    send_email_task.delay(to_email, subject, body)
    logger.info("📬 Email queued via Celery | To: %s", to_email)


def notify_booking_confirmed(
    background_tasks: BackgroundTasks,
    email: str, name: str, reference: str, title: str,
):
    body = f"Hi {name},\n\nBooking CONFIRMED!\nReference: {reference}\n{title}\n\nThanks,\nBooking System"
    background_tasks.add_task(_send_via_celery, email, f"Booking Confirmed — {reference}", body)


def notify_booking_cancelled(
    background_tasks: BackgroundTasks,
    email: str, name: str, reference: str, title: str,
):
    body = f"Hi {name},\n\nBooking CANCELLED.\nReference: {reference}\n{title}\n\nBooking System"
    background_tasks.add_task(_send_via_celery, email, f"Booking Cancelled — {reference}", body)


def notify_task_created(
    background_tasks: BackgroundTasks,
    email: str, name: str, task_title: str,
):
    body = f"Hi {name},\n\nNew task created: {task_title}\n\nBooking System"
    background_tasks.add_task(_send_via_celery, email, "New Task Created", body)