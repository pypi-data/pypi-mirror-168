""" The environment for the ordenario app. """
from aurori.workspaces import workspaceManager
from aurori.users import userManager
from aurori.messages.models import Message
from aurori.workspaces.models import Permission, PermissionGroup
from aurori.actions.models import ActionLink
from aurori.workspaces.workspaceHooks import WorkspaceHooks  # noqa: F401, F811 pylint: disable=W0611

#from aurori.users.defaultmodels import User
from workspaces.Users.models import User

def create_environment(_app, database, clean=False):
    """ Create the environment """

    print()
    print("Create environment")
    if clean is True:
        User.query.delete()
        PermissionGroup.query.delete()
        ActionLink.query.delete()
        Message.query.delete()

    all_permissions = Permission.query.all()
    permissions_dict = {}

    print("Detected permissions:")
    for permission in all_permissions:
        permissions_dict[permission.name] = permission

    sup_pg = PermissionGroup.query.filter_by(name="Supervisor").first()
    if sup_pg is None:
        sup_pg = PermissionGroup(name="Supervisor")
        sup_pg.permissions.append(permissions_dict["Log.ViewLogs"])        
        database.session.add(sup_pg)

    if User.query.filter_by(email="admin@fabba.space").first() is None:
        print("Create admin user")
        adminuser = User(email="admin@fabba.space", password="admin", isAdmin=True)
        adminuser.firstname = "Test"
        adminuser.lastname = "Admin"
        adminuser.organization = "Fabba Team"
        adminuser.account_activated = True
        adminuser.permission_groups.append(sup_pg)
        # adding the user to the database
        database.session.add(adminuser)
        # raise a event to inform about the creation
        userManager.raise_user_creation(adminuser)        

    all_permissions = Permission.query.all()
    print(all_permissions)

    database.session.commit()

    all_user = User.query.all()
    print(all_user)
