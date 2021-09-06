from datetime import datetime
from decimal import Decimal

import pytz
from django.utils import timezone

from economy.models import (
    CoinifyBalance,
    CoinifyInvoice,
    CoinifyPayout,
    EpayTransaction,
)


def import_epay_csv(csvreader):
    """Import an ePay CSV file. Assumes a CSV structure like this:

    "transactionID";"status";"merchantnumber";"orderID";"authamount";"currency";"authdate";"cardtypeID";"CompanyTransactionGroupID";"testTransaction";"FraudControl";"description";"CardHolder";"cardname";"display_short_name";"transaction_group_name";"CurrencyCodeA";"MinorUnit";"CurrencyName";"capturedamount";"creditedAmount";"capturedDate";"creditedDate";"isBooked";"fee";"tcardnumber";"authReferenceNumber"
    "212670400";"2";"1024488";"123";"1200.00";"208";"14-05-2019 19:37";"2";"0";"0";"0";"Order #123";"";"Visa/Dankort";"Visa/Dankort";"";"DKK";"2";"Danish Krone";"1200.00";"0.00";"14-05-2019 19:37";"";"1";"0.00";"098765XXXXXX0987";"20000"
    "213652781";"2";"1024488";"456";"1337.00";"208";"22-05-2019 17:58";"5";"0";"0";"0";"Order #456";"";"Mastercard (udenlandsk)";"MASTERCARD";"";"DKK";"2";"Danish Krone";"1337.00";"0.00";"22-05-2019 17:58";"";"1";"0.00";"543210XXXXXX4321";"20000"
    "214301864";"2";"1024488";"789";"1200.00";"208";"27-05-2019 21:31";"3";"0";"0";"0";"Order #789";"";"Visa/Electron (udenlandsk)";"VISA/ELECTRON";"";"DKK";"2";"Danish Krone";"1200.00";"0.00";"27-05-2019 21:31";"";"1";"0.00";"123456XXXXXX1234";"20000"

    Not all columns are imported. ePay CSV dialect includes a header line, is semicolon seperated, and uses "" for quoting.

    This function expects an initiated csvreader object, or alternatively some other iterable with the data in the right index locations.
    """
    cph = pytz.timezone("Europe/Copenhagen")
    create_count = 0
    # skip header row
    next(csvreader)
    for row in csvreader:
        et, created = EpayTransaction.objects.get_or_create(
            transaction_id=row[0],
            merchant_id=row[2],
            order_id=row[3],
            auth_amount=Decimal(row[4]),
            currency=row[16],
            auth_date=timezone.make_aware(
                datetime.strptime(row[6], "%d-%m-%Y %H:%M"),
                timezone=cph,
            ),
            description=row[11],
            card_type=row[13],
            captured_amount=Decimal(row[19]),
            captured_date=timezone.make_aware(
                datetime.strptime(row[21], "%d-%m-%Y %H:%M"),
                timezone=cph,
            ),
            transaction_fee=row[24],
        )
        if created:
            create_count += 1
    return create_count


class CoinifyCSVImporter:
    @staticmethod
    def import_coinify_invoice_csv(csvreader):
        """Import a CSV file with Coinify invoices exported from their webinterface.

        Assumes a CSV structure like this:

        id,id_alpha,created,payment_amount,payment_currency,payment_btc_amount,description,custom,credited_amount,credited_currency,state,payment_type,original_payment_id
        54276,sdJGd,"2020-02-06 16:53:51",1234,DKK,0.08345575,"BornHack order id #3527",{},154.94,EUR,complete,normal,
        54018,yfgGh,"2020-01-13 04:17:59",4567,DKK,0.07225667,"BornHack order id #7541",{},761.23,EUR,complete,normal,
        54430,dhdff,"2020-01-08 18:42:27",53459.02,DKK,0.0782233,"BornHack order id #3678",{},0.0782233,BTC,complete,extra,54554
        54448,4mWbd,"2020-01-05 18:27:44",1337,DKK,0.00233121,"BornHack order id #1234",{},178.77,EUR,complete,normal,

        The Coinify CSV dialect includes a header line, is comma seperated, and uses "" for quoting.

        This method expects an initiated csvreader object, or alternatively some other iterable with the data in the right index locations.
        """
        create_count = 0
        # skip header row
        next(csvreader)
        for row in csvreader:
            ci, created = CoinifyInvoice.objects.get_or_create(
                coinify_id=row[0],
                coinify_id_alpha=row[1],
                coinify_created=timezone.make_aware(
                    datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"),
                    timezone=timezone.utc,
                ),
                payment_amount=Decimal(row[3]),
                payment_currency=row[4],
                payment_btc_amount=Decimal(row[5]),
                description=row[6],
                custom=row[7],
                credited_amount=row[8],
                credited_currency=row[9],
                state=row[10],
                payment_type=row[11],
                original_payment_id=row[12] or None,
            )
            if created:
                create_count += 1
        return create_count

    @staticmethod
    def import_coinify_payout_csv(csvreader):
        """Import a CSV file with Coinify payouts exported from their webinterface.

        Assumes a CSV structure like this:

        id,created,amount,fee,transfer,currency,btc_txid
        124487,"2021-07-14 09:03:03",1116.1,0,1116.1,EUR,
        126509,"2021-08-25 10:59:13",1517.46,0,1517.46,EUR,

        The Coinify CSV dialect includes a header line, is comma seperated, and uses "" for quoting.

        This method expects an initiated csvreader object, or alternatively some other iterable with the data in the right index locations.
        """
        create_count = 0
        # skip header row
        next(csvreader)
        for row in csvreader:
            ci, created = CoinifyPayout.objects.get_or_create(
                coinify_id=row[0],
                coinify_created=timezone.make_aware(
                    datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"),
                    timezone=timezone.utc,
                ),
                amount=Decimal(row[2]),
                fee=Decimal(row[3]),
                transferred=Decimal(row[4]),
                currency=row[5],
                btc_txid=row[6] or None,
            )
            if created:
                create_count += 1
        return create_count

    @staticmethod
    def import_coinify_balance_csv(csvreader):
        """Import a CSV file with Coinify balances exported from their webinterface.

        Assumes a CSV structure like this:

        date,BTC,DKK,EUR
        2021-07-05,0.00000000,0.00,0.00
        2021-07-06,0.00000000,0.00,0.00
        2021-07-07,0.00000000,0.00,454.93
        2021-07-08,0.00000000,0.00,454.93
        2021-07-09,0.00000000,0.00,454.93
        2021-07-10,0.00000000,0.00,454.93
        2021-07-11,0.00000000,0.00,454.93
        2021-07-12,0.00000000,0.00,454.93
        2021-07-13,0.00000000,0.00,1116.10
        2021-07-14,0.00000000,0.00,1116.10
        2021-07-15,0.00000000,0.00,0.00
        2021-07-16,0.00000000,0.00,0.00

        The Coinify CSV dialect includes a header line, is comma seperated, and uses "" for quoting.

        This method expects an initiated csvreader object, or alternatively some other iterable with the data in the right index locations.
        """
        create_count = 0
        # skip header row
        next(csvreader)
        for row in csvreader:
            ci, created = CoinifyBalance.objects.get_or_create(
                date=row[0],
                btc=Decimal(row[1]),
                dkk=Decimal(row[2]),
                eur=Decimal(row[3]),
            )
            if created:
                create_count += 1
        return create_count