import html2text
import sendgrid
from sendgrid.helpers.mail import (
    ASM,
    Attachment,
    Category,
    Content,
    CustomArg,
    Email,
    Mail,
    Personalization,
)

from glibs.mail import Contact, File


class SendgridEmailClient(object):
    """By the usage of sendgrid-python 5.6.0, SendGrid requires an API key, which can be generated
    in their website.
    """

    def __init__(self, apikey):
        self.apikey = apikey

    def sendmail(self, *args, **kwargs):
        mail = self.__prepare_mail(*args, **kwargs)
        return self.__send_prepared_mail(mail)

    def __prepare_mail(
        self,
        recipients,
        sender,
        subject,
        message="",
        html="",
        category="",
        unique_arguments=None,
        undisclosed_recipients=(),
        unsubscribe_group_id=None,
        reply_to=None,
        attachments=None,
    ):
        sender_contact = Contact.new_from_parameter(sender)
        contacts = [Contact.new_from_parameter(recipient) for recipient in recipients]
        undisclosed_contacts = [
            Contact.new_from_parameter(recipient)
            for recipient in undisclosed_recipients
        ]

        sender = Email(**sender_contact.to_dict())

        personalization = Personalization()
        if len(contacts) == 0:
            # Sendgrid API forces you to have a recipient,
            # even if you have undisclosed recipients.
            personalization.add_to(Email(**sender_contact.to_dict()))
        else:
            for contact in contacts:
                personalization.add_to(Email(**contact.to_dict()))

        for contact in undisclosed_contacts:
            personalization.add_bcc(Email(**contact.to_dict()))

        mail = Mail()
        mail.from_email = sender
        mail.add_personalization(personalization)
        mail.subject = subject

        # (From SendGrid 5.6.0) Text content should be before HTML content
        if message:
            mail.add_content(Content("text/plain", message))
        else:
            h = html2text.HTML2Text()
            h.ignore_images = True
            h.ignore_tables = True
            plaintext = h.handle(html)
            mail.add_content(Content("text/plain", plaintext))
        if html:
            mail.add_content(Content("text/html", html))

        for index, recipient in enumerate(contacts):
            mail.add_custom_arg(
                CustomArg("Customer Emails {0}".format(index), recipient.email)
            )
        if unique_arguments:
            for unique_argument, argument_value in unique_arguments.items():
                mail.add_custom_arg(CustomArg(unique_argument, argument_value))

        if category:
            mail.add_category(Category(category))

        # By adding unsubscribe_group_id, sendgrid will automatically add links to the bottom of the
        # email. It can be customized in html, by using the tags <%asm_group_unsubscribe_raw_url%>
        # and <%asm_preferences_raw_url%>
        if unsubscribe_group_id:
            mail.asm = ASM(group_id=unsubscribe_group_id)

        if reply_to:
            reply_to_contact = Contact.new_from_parameter(reply_to)
            mail.reply_to = Email(**reply_to_contact.to_dict())

        if attachments and len(attachments) > 0:
            atts = [File.new_from_parameter(att) for att in attachments]
            for att in atts:
                attachment = Attachment()
                attachment.content = att.content
                attachment.type = att.type
                attachment.filename = att.file_name
                mail.add_attachment(attachment)

        return mail

    def __send_prepared_mail(self, mail):
        sg_client = sendgrid.SendGridAPIClient(apikey=self.apikey)

        return sg_client.client.mail.send.post(request_body=mail.get())
