from aurori.actions.action import Action
from aurori.logs import logManager
from aurori.actions import webclientActions

from aurori.actions import executeActionLink
from aurori.exceptions import NotFoundError, ExpiredError


class RunActionlink(Action):
    def __init__(self, app):
        # logManager.info("ProvideMenu of type Action created")
        super().__init__(app, uri="runActionlink")

    def handle(self, action, user, _workspace, _actionManager):
        logManager.info("Execute actionlink")
        response_actions = []
        try:
            response_actions.append(
                webclientActions.UpdateActionlinkStatusAction.generate(
                    "success", "Action succeed"
                )
            )
            response_actions = response_actions + executeActionLink(action.hash, user)
        except (ExpiredError, NotFoundError):
            response_actions = [
                webclientActions.UpdateActionlinkStatusAction.generate(
                    "error", "Action not found or expired"
                )
            ]
        except Exception as exception:
            logManager.error("Execute actionlink failed: {}".format(str(exception)))
            response_actions = [
                webclientActions.UpdateActionlinkStatusAction.generate(
                    "error", "Action failed"
                )
            ]

        return "success", response_actions
