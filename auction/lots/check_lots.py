from django.core.mail import send_mail

from auction import settings
from lots.models import Lot


def check_lots():
        lots = Lot.objects.filter(is_mail_send=False)

        for lot in lots:
            if not lot.is_available:
                letter_to_buyer = f"""
                Thank you for using our auction!\n
                You won the lot with the name {lot.heading}. Your bid {lot.bets.latest.set_price}.\n
                Please contact the seller to complete the transaction,
                here are the details:\n
                email: {lot.author.email}
                """
                letter_to_seller = f"""
                Thank you for using our auction!\n
                You salled lot with the name {lot.heading}. By bid {lot.bets.latest.set_price}.\n
                Please contact the buyer {lot.bets.set_by.username} to complete the transaction,
                here are the details:\n
                email: {lot.bets.set_by.email}
                """
                to_buyer = send_mail(
                    "You won the lot",
                    letter_to_buyer,
                    settings.ADMIN_EMAIL,
                    [lot.bets.set_by.email]
                )
                to_seller = send_mail(
                    "You sell lot",
                    letter_to_seller,
                    settings.ADMIN_EMAIL,
                    [lot.author.email]
                )
                if to_seller and to_buyer:
                    lot.is_mail_send = True
                    lot.save()
