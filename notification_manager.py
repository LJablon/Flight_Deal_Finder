from twilio.rest import Client
from credentials import *
import smtplib


class NotificationManager:

    def send_message(self, message_body):
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        if len(message_body) > 1599:
            message_body1 = message_body[:1500]
        else:
            message_body1 = message_body
        message = client.messages \
            .create(
                body=message_body1,
                from_=TWILIO_PHONE_NUMBER,
                to=MY_NUMBER,
            )
        print(message.status)

    def send_emails(self, message, mailing_list):

        if len(mailing_list) == 0:
            return
        for user in mailing_list:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(EMAIL, PASSWORD)
                connection.sendmail(from_addr=EMAIL, to_addrs=user["email"],
                                    msg=f"Subject:Low Price Flight Alert!\n\n{message}\n\nBest,\n\nFlight Finders Team")
