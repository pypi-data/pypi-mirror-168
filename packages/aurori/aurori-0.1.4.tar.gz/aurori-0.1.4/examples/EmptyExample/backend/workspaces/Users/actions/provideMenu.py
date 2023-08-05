from aurori.actions.action import Action
from aurori.logs import logManager
from aurori.actions import webclientActions


class ProvideMenu(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri="menu")

    def handle(self, action, user, workspace, actionManager):
        menuBuilder = actionManager.menuBuilder
        logManager.info("Execute registration action")

        # is this really necessary?
        # notification_action = webclientActions.NotificationAction.generate("Menu created", "info")
        notification_action = []
        menu = menuBuilder.buildMenu(user)
        updateMenu_action = webclientActions.UpdateMenuAction.generate(menu)
        return "success", [updateMenu_action, notification_action]
