from flask import request

from aurori.actions.action import Action
from aurori.actions import generateActionLink
from aurori.logs import logManager
from aurori.actions import webclientActions
from aurori.users import userManager
from aurori.messages import send_mail


class ResendVerificationRequest(Action):
    def __init__(self, app):
        super().__init__(app, uri="resendVerificationMail")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute resend activation mail action")
        notification_action = webclientActions.NotificationAction.generate(
            "The verification of your account got requested.", "success"
        )
        ref = request.referrer.split("/")
        if ref[0] != "http:" and ref[0] != "https:":
            ref = "/".join(ref[:1])
        else:
            ref = "/".join(ref[:3])

        verifyUser = userManager.getUser(action.username)
        if verifyUser is not None:
            link = generateActionLink(
                workspace,
                "verifyUser",
                {"email": verifyUser.email},
                "user/login",
                True,
                False,
            )
            data = {
                "username": verifyUser.firstname + " " + verifyUser.lastname,
                "action_link": link,
            }
            print(link)
            send_mail(
                [verifyUser.email],
                "Verify your account",
                workspace,
                "requestVerification.mail",
                data,
            )
        return "success", [notification_action]
