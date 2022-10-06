from datetime import datetime
from tokenize import group

groups = []

class User():
    def __init__(self, username):
        # TODO get an auto-generated userID from database
        self.username = username

    def join_group(self, group):
        # TODO make the member_id auto-increment
        new_dict = {6: self.user_name}
        group.member_ids.update(new_dict)

class Group():
    def __init__(self, member_ids, group_name, admin_id):
        self.member_ids = member_ids
        self.group_name = group_name
        self.admin_id = admin_id
        self.transactions = []
        self.payments = []
        groups.append(self)
        self.id = groups[-1]

    def add_transaction(self, payer_id, amount, description, transaction_creator):

        transaction = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
            "description": description, "transaction_creator": transaction_creator}
        self.transactions.append(transaction)

    def add_payment(self, payer_id, recipient_id, amount):

        payment = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
         "recipient_id": recipient_id}
        self.payments.append(payment)

    def announce_group(self):
        return (f" {self.group_name} has {len(self.member_ids)} members and the admin is {self.member_ids[str(self.admin_id)]}.")+\
        (f" Members: {self.member_ids} ")+ str(groups)

    def show_balance(self):
        balance = 0
        for transaction in self.transactions:
            balance += transaction['amount']
        print(f"{self.group_name} has a total balance of ${balance}.")

    def show_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def calculate_debts(self, member_id):
        
        total_paid = 0
        total_borrowed = 0

        for transaction in self.transactions:
            # if the member paid for the transaction, add to member's paid amount
            if transaction['payer_id'] == member_id:
                total_paid += transaction['amount']
            # add the amount to the member's borrowed amount
            total_borrowed += (transaction['amount'] / len(self.member_ids))

        for payment in self.payments:
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
            return (f"{self.member_ids[member_id]} borrowed {total_borrowed} and paid {total_paid}. They owe {owed_to_group}.")
        elif owed_to_group == 0:
            owed_to_group = "${:,.2f}".format(owed_to_group)
            return (f"{self.member_ids[member_id]} borrowed {total_borrowed} and paid {total_paid}. They are all settled up!")
        elif owed_to_group < 0:
            owed_to_group = owed_to_group * -1
            owed_to_group = "${:,.2f}".format(owed_to_group)
            return (f"{self.member_ids[member_id]} borrowed {total_borrowed} and paid {total_paid}. They are owed {owed_to_group}.")

