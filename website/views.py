from flask import Blueprint, request
from .models import Group, User, groups

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():

    return "Welcome to marmo."

@views.route('/create-group', methods=["POST"])
def create_group():
    # TODO add validation
    json = request.json
    admin_id = json["admin_id"]
    group_name = json["group_name"]
    member_ids = json["member_ids"]

    new_group = Group(admin_id=admin_id, group_name=group_name, member_ids=member_ids)
    
    return ("Group successfully created!"+\
        new_group.announce_group())

@views.route('create-user', methods=["POST"])
def create_user():
    # TODO add validation
    json = request.json
    username = json["username"]

    new_user = User(username=username)
    return f"New user successfully created with username: {new_user.username}."

@views.route('add-transaction', methods=["POST"])
def add_transaction():
    json = request.json

    group_id = int(json["group_id"])
    payer_id = json['payer_id']
    amount = float(json["amount"])
    description = json["description"]
    transaction_creator = json["transaction_creator"]
    
    groups[group_id].add_transaction(payer_id=payer_id, amount=amount, description=description, transaction_creator=transaction_creator)

    return f"Transaction for {amount} was successfully submitted to {groups[group_id].group_name}."

@views.route('calculate-debts', methods=["POST"])
def calculate_debts():
    json = request.json

    group_id = int(json["group_id"])
    member_id = json["member_id"]
    
    return groups[group_id].calculate_debts(member_id)
