from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

group_member = db.Table('group_member',
    db.Column('user.id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

user_transaction = db.Table('user_transaction',
    db.Column('user.id', db.Integer, db.ForeignKey('user.id')),
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    groups = db.relationship('Group', secondary=group_member, backref="members")
    transactions = db.relationship('Transaction', secondary=user_transaction, backref="members_included")

    def __repr__(self):
        return f'{self.username}'

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)
    group_name = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    transactions = db.relationship('Transaction')
    payments = db.relationship('Payment')

    def __repr__(self):
        return f'<Group: {self.group_name}>'

    def add_transaction(group_id, payer_id, amount, description, transaction_creator):

        transaction = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
            "description": description, "transaction_creator": transaction_creator}
        group_id.transactions.append(transaction)

    def add_payment(group_id, payer_id, recipient_id, amount):

        payment = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
            "recipient_id": recipient_id}
        group_id.payments.append(payment)
        for transaction in group_id.transactions:
            print(transaction)

    def calculate_debts(self, member):
        
        total_paid = 0
        total_borrowed = 0

        for transaction in self.transactions:
            # if the member paid for the transaction, add to member's paid amount
            if transaction.payer_id == member.id:
                total_paid += transaction.amount
            # add the amount to the member's borrowed amount
            if member in transaction.members_included:
                total_borrowed += (transaction.amount / len(transaction.members_included))

        overall = total_paid - total_borrowed

        for payment in self.payments:
             #if the member made a payment to another member, add to member's paid amount
            if payment.payer_id == member.id:
                overall += payment.amount
             #if the member received a payment from another member, add to member's borrowed amount
            if payment.recipient_id == member.id:
                overall -= payment.amount

        # round to nearest cent
        overall = round(overall, 2)

        return_list = [overall]
        if overall == 0:
            return_list.append(0)
        elif overall < 0:
            return_list.append(-1)
        elif overall > 0:
            return_list.append(1)
        return_list[0] = "{:,.2f}".format(abs(overall))
        return return_list

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    payer_id = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f'<Transaction: {self.description}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    payer_id = db.Column(db.Integer, nullable=False)
    recipient_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f'<Payment: {self.description}>'
