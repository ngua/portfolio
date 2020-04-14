from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import mail_admins


logger = get_task_logger(__name__)


@task(name='mail_admins_async')
def mail_admins_async(subject, message):
    logger.info('New email sent to admins via celery.')
    mail_admins(subject, message)
