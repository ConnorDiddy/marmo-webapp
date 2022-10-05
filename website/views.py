from flask import Blueprint, request
from .models import Group, User

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():

    return "view works"

@views.route('/create-group', methods=["POST"])
def create_group():
    json = request.json
    admin_id = json["admin_id"]
    group_name = json["group_name"]
    member_ids = json["member_ids"]

    new_group = Group(admin_id=admin_id, group_name=group_name, member_ids=member_ids)
    
    return ("Group successfully created!"+\
        new_group.announce_group())
