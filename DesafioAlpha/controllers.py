import threading
import time
import schedule

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

from DesafioAlpha import settings


def run_continuously(interval=500):
    """
    Run the schedule task continuously

    :param interval: interval in milliseconds
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()


def send_email_tunnel_breach(user: User, stock_name, sell_stock):
    template = 'tunnel_breach.html'
    context = {
        'user_name': user.first_name,
        'recommendation': 'VENDA' if sell_stock else 'COMPRA',
    }

    html_content = render_to_string(template, context)

    # get_connection allows getting SMTP variables
    connection = get_connection(
        host=settings.EMAIL['HOST'],
        use_tls=settings.EMAIL['USE_TLS'],
        port=settings.EMAIL['PORT'],
        username=settings.EMAIL['USER'],
        password=settings.EMAIL['PASSWORD']
    )

    # Preparing the email to be send
    message = EmailMultiAlternatives(
        subject=f'Temos uma atualização sobre a cotação \"{stock_name}\".',
        from_email=settings.FROM_EMAIL,
        to=(user.email,),
        connection=connection
    )

    message.attach_alternative(html_content, 'text/html')
    message.send()
