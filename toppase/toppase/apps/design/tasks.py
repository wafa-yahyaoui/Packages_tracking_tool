# from __future__ import absolute_import
#
# import sendgrid
# import os
# from sendgrid.helpers.mail import *
#
# from celery import task
#
# # from toppase.config.settings import API_KEY
# from .models import Mail as MyMail, MassMail
#
# @task()
# def send_emails(subject, message, sender, receivers, body, mass_mail_id):
#    """Send the mail to the receivers list using celery via SendGrid API
#    and saves it """
#    sg = sendgrid.SendGridAPIClient(apikey = API_KEY)
#    from_email = Email(sender)
#    subject = subject
#    content = Content("text/html", body)
#
#    for des in receivers:
#         to_email = Email(des)
#         mail = sendgrid.helpers.mail.Mail(from_email, subject, to_email, content)
#         mail.personalizations[0].add_custom_arg(
#                                   CustomArg("mass_mail_id", str(mass_mail_id))
#                                                 )
#         response = sg.client.mail.send.post(request_body=mail.get())
#
#         tracking = MyMail()
#         tracking.mass_mail = MassMail.objects.get(id=mass_mail_id)
#         tracking.receiver = des
#         tracking.save()
#
#
#
#
#
#
#
