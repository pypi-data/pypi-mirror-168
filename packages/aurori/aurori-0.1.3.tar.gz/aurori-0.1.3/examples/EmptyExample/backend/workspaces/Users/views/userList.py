from aurori.workspaces import DataView, Workspace

from workspaces.Users.models import User
""" A view contaning a list of all users not locked
"""


class UserList(DataView):

    uri = 'userList'
    requireLogin = True

    def defineMetadata(self):
        self.addStringMeta("test")

    def defineProperties(self):
        self.addMailProperty(name='email', label='eMail', isKey=True)
        self.addIntegerProperty(name='id', label='ID')
        self.addStringProperty(name='name', label='Name')
        self.addStringProperty(name='organization', label='Organization')
        self.addIntegerProperty(name='orderlimit', label='Order limit')
        self.addSelectProperty(name='ldap',
                               selectables=lambda: ['Yes', 'No'],
                               label='LDAP')
        self.addActionProperty(name='lock',
                               label='Lock user',
                               action='lock',
                               actionHandler=self.lockHandler,
                               icon='clear')
        self.addActionProperty(name='setAdmin',
                               action='setAdmin',
                               actionHandler=self.setAdmin,
                               label='Give admin privileges',
                               icon='flash_on',
                               color="green")
        self.addActionProperty(name='unsetAdmin',
                               actionHandler=self.unsetAdmin,
                               label='Remove admin privileges',
                               action='unsetAdmin',
                               icon='flash_off')

    def getViewHandler(self, user: User, _workspace: Workspace, _query=None):
        print("getDataViewHandler for UserView")
        userlist = []
        all_user = User.query.filter_by(account_locked=False).all()
        for u in all_user:

            assert isinstance(u, User)
            # get new empty entry
            entry = self.createEntry()

            # fill entry
            entry.id = u.id
            entry.email = u.email
            entry.name = "{0} {1}".format(u.firstname, u.lastname)
            entry.organization = u.organization
            entry.orderlimit = u.orderlimit
            entry.ldap = 'Yes' if u.ldap else 'No'

            # set entry actions
            entry.lock = False

            if user.admin is True and u.admin is False:
                entry.lock = True
                entry.setAdmin = True
                entry.unsetAdmin = False

            if user.admin is True and u.admin is True:
                entry.setAdmin = False
                entry.unsetAdmin = True

            userlist.append(entry.extract())
        userlist = sorted(userlist, key=lambda item: item['name'])
        return userlist

    # Handler for a request to update a single view entry
    def updateViewEntryHandler(self, user, _workspace, key, entry):
        user = User.query.filter_by(email=key).first()
        user.orderlimit = entry.orderlimit

        self.emitSyncUpdate(key)
        print("Handle updateViewEntryHandler request for User order limit")

    def lockHandler(self, _user, _workspace, _action, entrykey):
        locked_user = User.query.filter_by(email=entrykey).first()
        locked_user.account_locked = True
        self.emitSyncCreate(entrykey, "userLockedList")
        self.emitSyncRemove(entrykey, "userList")
        return {"a": 1}

    def __repr__(self):
        return '<{} with {} properties>'.format(self.name,
                                                len(self.properties))

    # Handler for a request to create a new view entry
    def createViewEntryHandler(self, user, workspace):
        print("Handle createViewEntry request for UserListView")

    # give user admin priviliges
    def setAdmin(self, user, _workspace, _action, key):
        user = User.query.filter_by(email=key).first()
        user.admin = True
        self.emitSyncUpdate(key, "userList")

    # remove user admin priviliges
    def unsetAdmin(self, user, _workspace, _action, key):
        user = User.query.filter_by(email=key).first()
        user.admin = False
        self.emitSyncUpdate(key, "userList")
