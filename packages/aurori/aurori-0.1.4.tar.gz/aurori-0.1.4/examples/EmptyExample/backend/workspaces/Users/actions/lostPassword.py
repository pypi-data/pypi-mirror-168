from flask import request
import arrow
import random
import string
from aurori.actions.action import Action
from aurori.logs import logManager
from aurori.actions import webclientActions
from aurori.users import userManager
from aurori.messages import send_mail


class LostPassword(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri="lostPassword")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute lost password action")
        notification_action = webclientActions.NotificationAction.generate(
            "A email to reset the password will be send to you", "success"
        )
        ref = request.referrer.split("/")
        if ref[0] != "http:" and ref[0] != "https:":
            ref = "/".join(ref[:1])
        else:
            ref = "/".join(ref[:3])

        resetUser = userManager.getUser(action.username)
        if resetUser is not None:
            key = "".join(random.choices(string.ascii_letters + string.digits, k=96))
            resetUser.password_reset_expired_date = arrow.utcnow().shift(hours=2)
            resetUser.password_reset_hash = key
            link = ref + "/user/resetpassword" + "?key=" + key
            data = {
                "username": resetUser.firstname + " " + resetUser.lastname,
                "reset_link": link,
            }
            print(key)
            send_mail(
                [resetUser.email],
                "Reset your password",
                workspace,
                "lostPassword.mail",
                data,
            )

        return "success", [notification_action]
