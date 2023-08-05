from aurori.workspaces import DataView, Workspace
from aurori.users import userManager

from workspaces.Users.models import User

""" A view contaning a list of all users locked
"""


class UserLockedList(DataView):

    uri = "userLockedList"
    requireLogin = True

    def defineProperties(self):
        self.addMailProperty(name="email", label="eMail", isKey=True)
        self.addStringProperty(name="name", label="Name")
        self.addActionProperty(
            name="unlock",
            label="Unlock user",
            action="unlock",
            actionHandler=self.unlockHandler,
            color="green",
            icon="undo",
        )
        self.addActionProperty(
            name="remove",
            label="Remove user",
            action="remove",
            actionHandler=self.removeHandler,
            icon="clear",
        )

    def getViewHandler(self, user: User, workspace: Workspace, query=None):
        print("getDataViewHandler for UserView")
        userlist = []
        all_user = User.query.filter_by(account_locked=True).all()
        for u in all_user:
            assert isinstance(u, User)

            # get new empty entry
            entry = self.createEntry()

            # fill entry data
            entry.email = u.email
            entry.name = "{0} {1}".format(u.firstname, u.lastname)

            # set entry actions
            entry.remove = True
            entry.unlock = True
            userlist.append(entry.extract())
        return userlist

    def removeHandler(self, _user, _workspace, _action, entrykey):
        userManager.removeUser(entrykey)
        self.emitSyncRemove(entrykey, "userLockedList")

    def unlockHandler(self, user, workspace, action, entrykey):
        locked_user = User.query.filter_by(email=entrykey).first()
        locked_user.account_locked = False
        self.emitSyncCreate(entrykey, "userList")
        self.emitSyncRemove(entrykey, "userLockedList")

    def __repr__(self):
        return "<{} with {} properties>".format(self.name, len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace, entry):
        print("Handle createViewEntry request for " + self.uri)

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, workspace, key, entry):
        print("Handle updateViewEntryHandler request for " + self.uri)
