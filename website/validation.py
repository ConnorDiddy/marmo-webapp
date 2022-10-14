from .models import Group, User

class Validation():

    def check_description(string):
        if len(string) < 1 or string == None:
            raise ValueError("Description cannot be empty.")
        if len(string) > 255:
            raise ValueError("Length of description cannot exceed 255 characters.")

    def check_user_id(id):
        if len(str(id)) < 1 or id == None or int(id) < 1:
            raise ValueError("UserID field cannot be empty.")
        if User.query.filter_by(id=id).first() == None:
            raise ValueError(f"User with id: {id} does not exist")

    def check_group_id(id):
        if len(str(id)) < 1 or id == None or int(id) < 1:
            raise ValueError("GroupID field cannot be empty.")
        if Group.query.filter_by(id=id).first() == None:
            raise ValueError(f"Group with id: {id} does not exist")

    def check_amount(amount):
        if len(amount) < 1 or amount == None:
            raise ValueError("Amount cannot be empty.")
        if float(amount) <= 0:
            raise ValueError("Amount must be greater than 0.")

    def join_group(group_id, user):
        Validation.check_group_id(group_id)

        for group in user.groups:
            if int(group.id) == int(group_id):
                raise ValueError("You are already in this group, silly head!")

    def add_transaction(payer_id, amount, description, creator_id, group_id, members_submitted):
        Validation.check_user_id(payer_id)
        Validation.check_user_id(creator_id)
        Validation.check_group_id(group_id)
        Validation.check_amount(amount)
        Validation.check_description(description)

        if members_submitted == []:
            raise ValueError("You must select at least one person responsible for paying for this transaction.")

    def add_payment(payer_id, amount, recipient_id, description):
        Validation.check_user_id(payer_id)
        Validation.check_amount(amount)
        Validation.check_user_id(recipient_id)
        Validation.check_description(description)

        if payer_id == recipient_id:
            raise ValueError("Payer and recipient cannot be the same person.")

    def create_group(group_name):
        if len(group_name) < 1 or group_name == None:
            raise ValueError("Group name cannot be empty.")
        elif len(group_name) > 50:
            raise ValueError("Group name cannot exceed 50 characters.") 