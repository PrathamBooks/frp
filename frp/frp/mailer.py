"""
Implements the mailer object which can be used
"""

import socket

from flask import render_template, current_app
from flask_mail import Mail as FlaskMail, Message as FlaskMailMessage
from flask.ext.sendmail import Mail as FlaskSendmail, Message as FlaskSendmailMessage

class Mailer(object):
    def send_email(self, to, subject, template, **vals):
        """
        Send email to `to` from the default from address using the
        given `template` (which should be a file under the 'email'
        subdirectory of templates) and the provided subject. All other
        values are used to fill in the template.
        """
        if not isinstance(to, list):
            to = [to]
        message_content = render_template("email/{}".format(template), **vals)
        if current_app.config.get('DEBUG', True):
            print "------------------- Email ------------------ "
            print "To:{}".format(",".join(to))
            print "Subject: {}".format(subject)
            print message_content
            print "------------------- End ------------------ "
            return
        try:
            message = FlaskMailMessage(body = message_content,
                                       subject = subject,
                                       recipients = to)
            mail_engine = current_app.extensions.get('mail', None)
            mail_engine.send(message)
        except socket.error:
            print "Trying sendmail callback"

            message = FlaskSendmailMessage(body = message_content,
                                           subject = subject,
                                           recipients = to)
            self.flask_sendmail.send(message)
        print "Mail sent"
