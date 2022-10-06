from datetime import datetime
from unicodedata import name
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, nullable=False)
    group_name = db.Column(db.String(30), nullable=False)

    def add_transaction(group_id, payer_id, amount, description, transaction_creator):

        transaction = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
            "description": description, "transaction_creator": transaction_creator}
        group_id.transactions.append(transaction)

    def add_payment(group_id, payer_id, recipient_id, amount):

        payment = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
            "recipient_id": recipient_id}
        group_id.payments.append(payment)

    def announce_group(group_id):
        return (f" {group_id.group_name} has {len(group_id.member_ids)} members and the admin is {group_id.member_ids[str(group_id.admin_id)]}.")+\
        (f" Members: {group_id.member_ids} ")

    def show_balance(group_id):
        balance = 0
        for transaction in group_id.transactions:
            balance += transaction['amount']
        print(f"{group_id.group_name} has a total balance of ${balance}.")

    def show_transactions(group_id):
        for transaction in group_id.transactions:
            print(transaction)

    def calculate_debts(group_id, member_id):
        
        total_paid = 0
        total_borrowed = 0

        for transaction in group_id.transactions:
            # if the member paid for the transaction, add to member's paid amount
            if transaction['payer_id'] == member_id:
                total_paid += transaction['amount']
            # add the amount to the member's borrowed amount
            total_borrowed += (transaction['amount'] / len(group_id.member_ids))

        for payment in group_id.payments:
            # if the member made a payment to another member, add to member's paid amount
            if payment['payer_id'] == member_id:
                total_paid += payment['amount']
            # if the member received a payment from another member, add to member's borrowed amount
            if payment['recipient_id'] == member_id:
                total_borrowed += payment['amount']

        owed_to_group = total_borrowed - total_paid
        total_borrowed = "${:,.2f}".format(total_borrowed)
        total_paid = "${:,.2f}".format(total_paid)

        if owed_to_group > 0:
            owed_to_group = "${:,.2f}".format(owed_to_group)
            return (f"{group_id.member_ids[member_id]} borrowed {total_borrowed} and paid {total_paid}. They owe {owed_to_group}.")
        elif owed_to_group == 0:
            owed_to_group = "${:,.2f}".format(owed_to_group)
            return (f"{group_id.member_ids[member_id]} borrowed {total_borrowed} and paid {total_paid}. They are all settled up!")
        elif owed_to_group < 0:
            owed_to_group = owed_to_group * -1
            owed_to_group = "${:,.2f}".format(owed_to_group)
            return (f"{group_id.member_ids[member_id]} borrowed {total_borrowed} and paid {total_paid}. They are owed {owed_to_group}.")

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payer_id = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300), nullable=False)

