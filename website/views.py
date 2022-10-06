from sre_constants import SUCCESS
from flask import Blueprint, request, render_template, flash
from .models import Group, User
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("home.html", user=current_user)

@views.route('/create-group', methods=["GET", "POST"])
@login_required
def create_group():
    if request.method == "POST":
        # TODO add validation
        json = request.json
        admin_id = current_user.id
        group_name = request.form.get('group_name')
        #member_ids = request.form.get('member_ids')

        new_group = Group(admin_id=admin_id, group_name=group_name)
        db.session.add(new_group)
        db.session.commit()
        flash(f"Group {new_group.group_name} successfully created!", category=SUCCESS)
    
    return render_template("create_group.html", user=current_user)

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

@views.route('search-users', methods=["GET"])
def search_user():
    json = request.json
    users = []
    result = str(User.query.all())

    #for user in result:
        #user_dict = {}
       # user_dict["id"] = user.id
        #user_dict["username"] = user.username
       # user_dict["email"] = user.email
       # user_dict["date_created"] = user.date_created
       # users.append(user_dict)

    return result.id