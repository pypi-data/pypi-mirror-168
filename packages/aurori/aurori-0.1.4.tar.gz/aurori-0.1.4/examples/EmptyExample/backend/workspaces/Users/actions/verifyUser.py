from aurori.actions.action import Action
from aurori.logs import logManager

from workspaces.Users.models import User


class VerifyUser(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri='verifyUser')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Request user verification")
        user = User.query.filter_by(email=action.email).first()

        if user is None:
            raise Exception("User not found")

        user.account_verified = True
        return 'success', []

    @staticmethod
    def generate(**kwargs):
        return kwargs
