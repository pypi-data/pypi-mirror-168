import arrow
from aurori.actions.action import Action
from aurori.logs import logManager
from aurori.actions import webclientActions

from workspaces.Users.models import User

class ResetPassword(Action):
    def __init__(self, app):
        super().__init__(app, uri="resetPassword")

    def handle(self, action, user, workspace, actionManager):
        user = User.query.filter_by(password_reset_hash=action.resetKey).first()
        if user is None:
            notification_action = webclientActions.NotificationAction.generate(
                "Key is not valid or expired", "error"
            )
        else:
            if user.password_reset_expired_date < arrow.utcnow():
                notification_action = webclientActions.NotificationAction.generate(
                    "Key is not valid or expired", "error"
                )
            else:
                notification_action = webclientActions.NotificationAction.generate(
                    "Password changed", "success"
                )
                user.password = action.password

        logManager.info("Request password reset", user)
        return "success", [notification_action]
