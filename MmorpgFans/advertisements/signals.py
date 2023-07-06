from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
# from django.core.mail import mail_managers
from .models import Respond, Advert

from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives

from django.conf import settings
 

def get_user_emails():
    user_emails=[]
    for user in Advert.author.all():
        user_emails.append(user.email)
    return user_emails


@receiver(post_save, sender=Respond)
def notify_respond_new_or_accept(sender, instance, created, update_fields, **kwargs):
    if created:
        # # новый отклик - оповещаем автора объявления
        # print('Новый отклик ')
        # print(instance.advert.author.username)
        # print(instance.advert.title)
        template='respond_new.html'
        email_subject=f"Новый отклик на ваше объявление: {instance.advert.title}"
        user_emails=instance.advert.author.email
        html_content=render_to_string(
            template_name=template,
            context={
                # 'advert': instance.advert.author,
                'respond': instance,
                'site_url': 'http://127.0.0.1:8000/advertisements/',
            }
        ) 
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_emails,],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        # иначе - изменение (нужно, что изменилось поле accept) - оповещаем автора отклика
        if update_fields is not None and 'accept' in update_fields:  # and update_fields['accept']:
            if instance.accept:
                template='respond_accept.html'
                email_subject=f"Ваш отклик на объявление принят."
                user_emails=instance.author.email
                html_content=render_to_string(
                    template_name=template,
                    context={
                        'respond': instance,
                        'site_url': 'http://127.0.0.1:8000/advertisements/',
                    }
                ) 
                msg = EmailMultiAlternatives(
                    subject=email_subject,
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user_emails,],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
