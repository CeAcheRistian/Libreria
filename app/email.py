from flask_mail import Message
from flask import current_app, render_template

from threading import Thread


def purchase_confirmation(app, mail, user, book) -> None:
    try:
        message = Message(
            'Confirmación de compra',
            sender = current_app.config['MAIL_USERNAME'],
            recipients = ['666monroy@gmail.com'])
        
        message.html = render_template('emails/purchase_confirmation.html', user=user, book=book)
        
        thread = Thread(target=email_async, args=[app, mail, message])
        thread.start()

    except Exception as ex:
        raise Exception(ex)


def email_async(app, mail, message):
    with app.app_context():
        mail.send(message)