
from sre_constants import FAILURE, SUCCESS
from flask import Blueprint, request, render_template, flash, redirect
from .models import Group, User, Transaction, Payment
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if (str(current_user)[0] != '<'):
        return render_template("home.html", user=current_user)
    else:
        return render_template("landing.html", user=current_user)

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

@views.route('add-transaction', methods=["GET","POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        payer_id = request.form.get('payer_id')
        amount = request.form.get('amount')
        description = request.form.get('description')
        creator_id = current_user.id
        group_id = request.form.get('group_id')
        members_submitted = request.form.getlist('member_included')
        group = Group.query.filter_by(id=group_id).first()

        members_included = []
        for member in members_submitted:
            member = User.query.filter_by(id=int(member)).first()
            members_included.append(member)
        if members_included == []:
            flash("You must include at least one member who is responsible for paying.", category='error')

            return render_template("add_transaction.html", user=current_user, group=group)
        else:
            new_transaction = Transaction(payer_id=payer_id, amount=amount, description=description,\
                creator_id=creator_id, group_id=group_id, members_included=members_included)
            db.session.add(new_transaction)
            db.session.commit()
            flash(f"Transaction for ${new_transaction.amount} successfully submitted to {group.group_name}!", category=SUCCESS)

        return redirect(f"http://127.0.0.1:5000/mygroup?groupID={group.id}")

    if request.method == "GET":
        group_id = request.args['groupID']
        group = Group.query.filter_by(id=group_id).first()

        return render_template('add_transaction.html', user=current_user, group=group)

@views.route('add-payment', methods=["GET","POST"])
@login_required
def payment():
    if request.method == "POST":
        payer_id = request.form.get('payer_id')
        group_id = request.form.get('group_id')
        amount = request.form.get('amount')
        recipient_id = request.form.get('recipient_id')
        description = request.form.get('description')
        recipient = User.query.filter_by(id=recipient_id).first()
        group = Group.query.filter_by(id=group_id).first()

        new_payment = Payment(payer_id=payer_id, amount=amount, \
            recipient_id=recipient_id, group_id=group_id, description=description)
        db.session.add(new_payment)
        db.session.commit()
        flash(f"Payment of ${new_payment.amount} to {recipient.username} successfully submitted!", category=SUCCESS)
        return redirect(f"http://127.0.0.1:5000/mygroup?groupID={group.id}")

    if request.method == "GET":
        group_id = request.args['groupID']
        group = Group.query.filter_by(id=group_id).first()

        return render_template('add_payment.html', user=current_user, group=group)

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

@views.route('mygroup', methods=["GET"])
def show_group():
    if request.method == "GET":
        group_id = request.args['groupID']
        group = Group.query.filter_by(id=group_id).first()

        return render_template("group.html", user=current_user, group=group)

@views.route('see-transactions', methods=["GET"])
def show_transactions():
    group_id = request.args['groupID']
    group = Group.query.filter_by(id=group_id).first()

    return render_template('see_transactions.html', user=current_user, group=group)

@views.route('delete-transaction', methods=["GET"])
@login_required
def delete_transaction():
    transaction_id = request.args['tranID']
    group_id = request.args['groupID']
    group = Group.query.filter_by(id=group_id).first()
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    db.session.delete(transaction)
    db.session.commit()

    return render_template('see_transactions.html', user=current_user, group=group)

@views.route('delete-payment', methods=["GET"])
@login_required
def delete_payment():
    payment_id = request.args['paymentID']
    group_id = request.args['groupID']
    group = Group.query.filter_by(id=group_id).first()
    payment = Payment.query.filter_by(id=payment_id).first()
    db.session.delete(payment)
    db.session.commit()

    return render_template('see_transactions.html', user=current_user, group=group)

@views.route('leave-group', methods=["GET"])
@login_required
def leave_group():
    member_id = request.args['memberID']
    group_id = request.args['groupID']
    group = Group.query.filter_by(id=group_id).first()
    member = User.query.filter_by(id=member_id).first()

    member.groups.remove(group)

    if group.members == []:
        db.session.delete(group)
    elif group.admin_id == member.id:
        group.admin_id = group.members[0].id
    db.session.commit()
    flash(f"You have left {group.group_name}.", category=SUCCESS)

    return home()

@views.route('delete-group', methods=["GET"])
@login_required
def delete_group():
    member_id = request.args['memberID']
    group_id = request.args['groupID']
    group = Group.query.filter_by(id=group_id).first()
    member = User.query.filter_by(id=member_id).first()

    if group.admin_id == member.id:
        db.session.delete(group)
        db.session.commit()
        flash(f"{group.group_name} has been deleted.", category=SUCCESS)
    else:
        flash(f"You must be the admin to be able to delete this group.", category=FAILURE)

    return home()

@views.route('account', methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html", user=current_user)

@views.route('delete-account', methods=["GET"])
@login_required
def delete_account():
    user_id = request.args['id']
    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()

    return home()

@views.route('/base')
def base():
    return "The base page for users not logged in. <a href='login'>Log in</a>"

@views.route('style.css')
def stylesheet():
    return "templates/style.css"