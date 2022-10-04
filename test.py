# redrockridge_members = {1: 'Connor', 2: 'Carson', 3: 'Max', 4: 'Mckade', 5: 'Charley'}
# Group's object name is the ID of the group
# Transaction is defined as a purchase made by a member for the group
# Payment is defined as a transfer of money by a member to settle up with other members

from datetime import datetime

class Group():
    def __init__(self, member_ids, group_name, admin_id):
        self.member_ids = member_ids
        self.group_name = group_name
        self.admin_id = admin_id
        self.transactions = []
        self.payments = []

    def add_transaction(self, payer_id, amount, description, transaction_creator):

        transaction = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
            "description": description, "transaction_creator": transaction_creator}
        self.transactions.append(transaction)

    def add_payment(self, payer_id, recipient_id, amount):

        payment = {"date": datetime.now(), "payer_id": payer_id, "amount": amount, \
         "recipient_id": recipient_id}
        self.payments.append(payment)

    def announce_group(self):
        print(f"{self.group_name} has {len(self.member_ids)} members and the admin is {rrr_id.member_ids[rrr_id.admin_id]}.")
        print(f"Members: {self.member_ids}")

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

        # TODO for payment in self.payments:

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

    
class User():
    def __init__(self, user_name):
        # TODO get an auto-generated userID from database
        self.user_name = user_name

    def join_group(self, group):
        # TODO make the member_id auto-increment
        new_dict = {6: self.user_name}
        group.member_ids.update(new_dict)

deangelo_id = User('DeAngelo')

rrr_id = Group({1: 'Connor', 2: 'Carson', 3: 'Max', 4: 'Mckade', 5: 'Charley'}, 'RedRock', 1)
rrr_id.announce_group()

# deangelo_id.join_group(rrr_id)
# rrr_id.announce_group()

rrr_id.add_transaction(5, 120, 'Rotisserie Chicken', 5)
rrr_id.add_transaction(4, 69, 'Bananas', 2)

print(rrr_id.calculate_debts(1))
print(rrr_id.calculate_debts(2))
print(rrr_id.calculate_debts(3))
print(rrr_id.calculate_debts(4))
print(rrr_id.calculate_debts(5))

rrr_id.add_transaction(1, 38.7, 'Cash deposit', 1)


#rrr_id.announce_group()
rrr_id.show_balance()
rrr_id.show_transactions()

print(rrr_id.calculate_debts(1))
print(rrr_id.calculate_debts(2))
print(rrr_id.calculate_debts(3))
print(rrr_id.calculate_debts(4))
print(rrr_id.calculate_debts(5))

