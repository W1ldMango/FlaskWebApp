from services.models import myapp_user
from werkzeug.security import generate_password_hash, check_password_hash

# usr = "admin"
# pwd = "123"


# def create_user(username, password):
#     new_user = myapp_user.User(username=username, password=generate_password_hash(password, method='sha256'))
#     db.session.add(new_user)
#     db.session.commit()
#
# create_user(usr, pwd)
# create_user("admin2", "1234")

#
#
# def is_valid(username, passwd):
#     return username == usr and passwd == pwd
