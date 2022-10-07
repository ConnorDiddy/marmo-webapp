
from sre_constants import SUCCESS
from flask import Blueprint, request, render_template, flash
from .models import Group, User, Transaction
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
        admin_id = current_user.id
        group_name = request.form.get('group_name')

        new_group = Group(admin_id=admin_id, group_name=group_name)
        current_user.groups.append(new_group)
        db.session.add(new_group)
        db.session.commit()
        flash(f"Group {new_group.group_name} successfully created!", category=SUCCESS)

        return home()
    
    return render_template("create_group.html", user=current_user)

@views.route('join-group', methods=["GET","POST"])
@login_required
def join_group():
    if request.method == "POST":
        group_id = request.form.get('group_id')

        group = Group.query.filter_by(id=group_id).first()
        current_user.groups.append(group)
        db.session.commit()
        flash(f"User {current_user.username} successfully joined {group.group_name}!", category=SUCCESS)

        return home()

    return render_template("join_group.html", user=current_user)

@views.route('add-transaction', methods=["POST"])
def add_transaction():
    json = request.json

    group_id = int(json["group_id"])
    group = Group.query.filter_by(id=group_id).first()
    payer_id = json['payer_id']
    amount = float(json["amount"])
    description = json["description"]
    creator_id = json["creator_id"]
    
    new_transaction = Transaction(payer_id=payer_id, amount=amount, description=description,\
         creator_id=creator_id, group_id=group_id)
    db.session.add(new_transaction)
    db.session.commit()
    return f"Transaction for ${new_transaction.amount} was successfully submitted to {group.group_name}."

@views.route('calculate-debts', methods=["POST"])
def calculate_debts():
    json = request.json

    group_id = int(json["group_id"])
    group = Group.query.filter_by(id=group_id).first()
    member_id = json["member_id"]
    member = User.query.filter_by(id=member_id).first()
    
    return group.calculate_debts(member)

@views.route('search-users', methods=["GET", "POST"])
def search_user():
    return_dict = {}
    if request.method == "POST":
        json = request.json
        id = json["id"]
        return_user = User.query.filter_by(id=id).first()
        return_dict["id"] = return_user.id
        return_dict["username"] = return_user.username
        return_dict["email"] = return_user.email
        return_dict["date_created"] = return_user.date_created
        return_dict["groups"] = str(return_user.groups)
    else:
        all_users = User.query.all()
        
        for user in all_users:
            return_dict[user.id] = user.username

    return return_dict

@views.route('search-groups', methods=["GET", "POST"])
def search_groups():
    return_dict = {}
    if request.method == "POST":
        json = request.json
        id = json["id"]
        return_group = Group.query.filter_by(id=id).first()
        return_dict["id"] = return_group.id
        return_dict["group_name"] = return_group.group_name
        return_dict["admin_id"] = return_group.admin_id
        return_dict["date_created"] = return_group.date_created
        return_dict["members"] = str(return_group.members)
        return_dict["transactions"] = str(return_group.transactions)
    else:
        all_groups = Group.query.all()
        
        for group in all_groups:
            return_dict[group.id] = group.group_name

    return return_dict