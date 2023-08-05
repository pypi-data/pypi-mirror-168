from aurori.actions.action import Action
from aurori.logs import logManager
from aurori.actions import webclientActions
from aurori.users import userManager
from aurori.messages import send_mail, send_message
from aurori.actions import generateActionLink


class Register(Action):
    def __init__(self, app):
        # logManager.info("Register of type Action created")
        super().__init__(app, uri="register")

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute registration action")
        replyActions = []
        userdata = action["userdata"]
        if userManager.checkUserExist(userdata["email"]):
            replyActions.append(
                webclientActions.NotificationAction.generate(
                    "User already exist", "error"
                )
            )
        else:
            u = userManager.register_user(userdata)
            link = generateActionLink(
                workspace,
                "verifyUser",
                {"email": userdata["email"]},
                "user/login",
                True,
                False,
            )
            data = {
                "username": userdata["firstname"] + " " + userdata["lastname"],
                "action_link": link,
            }
            send_mail(
                [userdata["email"]],
                "Verify your account",
                workspace,
                "requestVerification.mail",
                data,
            )
            send_message(
                u,
                "Welcome",
                workspace,
                "welcome.message",
                data,
                "aurori",
                False,
                "welcome.mail",
            )
            replyActions.append(
                webclientActions.NotificationAction.generate(
                    "User registered", "success"
                )
            )
            replyActions.append(webclientActions.RouteAction.generate("dashboard", 3))

        return "success", replyActions
