import datetime
import arrow
from flask_jwt_extended import create_access_token
import re
import json

from aurori.actions.action import Action
from aurori.logs import logManager
from aurori.actions import webclientActions
from aurori.monits import monit_manager

from workspaces.Users.monits import UserLoginEvent


class Login(Action):
    def __init__(self, app):
        # logManager.info("Login of type Action created")
        super().__init__(app, uri='login')

    def handle(self, action, user, workspace, actionManager):
        logManager.info("Execute login action")
        replyActions = []
        user = (actionManager.userManager.getUser(action['username']))
        if user is not None:
            if (actionManager.userManager.checkUserPassword(
                    user, action['password'])):
                menuBuilder = actionManager.menuBuilder
                # create jwt token
                expires = datetime.timedelta(days=1)
                access_token = create_access_token(identity=action['username'],
                                                   expires_delta=expires)
                # update menu
                menu = menuBuilder.buildMenu(user)
                # build up
                userinfo = {
                    'email': user.email,
                    'limit': user.orderlimit,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                }
                replyActions.append(
                    webclientActions.UpdateSessionTokenAction.generate(
                        access_token, userinfo))
                replyActions.append(
                    webclientActions.UpdateMenuAction.generate(menu))
                replyActions.append(
                    webclientActions.NotificationAction.generate(
                        "Login successful.", "success"))

                # fixme: this doesn't handle given routes, but does the same as the other case
                if 'route' in action['options']:
                    if action['options']['route'] is True:
                        replyActions.append(
                            webclientActions.RouteAction.generate(
                                "dashboard", 3))
                elif 'params' in action['options'] and 'next' in action[
                        'options']['params']:
                    # this is the working forward with fallback
                    try:
                        parameter_string = ''
                        if 'query_parameters' in action['options']['params']:
                            parameter_dict = json.loads(
                                action['options']['params']
                                ['query_parameters'])
                            parameter_list = []
                            try:
                                for param, value in parameter_dict.items():
                                    # fixme: sanitize parameters?
                                    parameter_list.append('{}={}'.format(
                                        param, value))
                            except Exception:
                                pass
                            if len(parameter_list) > 0:
                                parameter_string = '?{}'.format(
                                    '&'.join(parameter_list))
                        forward_page = '{}{}'.format(
                            re.sub('^/', '',
                                   action['options']['params']['next']),
                            parameter_string,
                        )
                        replyActions.append(
                            webclientActions.RouteAction.generate(
                                forward_page))
                    except Exception:
                        replyActions.append(
                            webclientActions.RouteAction.generate("dashboard"))
                else:
                    replyActions.append(
                        webclientActions.RouteAction.generate("dashboard"))

                user.sessionValid = True
                user.last_login_date = arrow.utcnow()
                monit_manager.raise_monitor_event(
                    UserLoginEvent(1, "successful"))
            else:
                monit_manager.raise_monitor_event(UserLoginEvent(1, "failed"))
                replyActions.append(
                    webclientActions.NotificationAction.generate(
                        "Login failed with username or password.", "error"))
        else:
            replyActions.append(
                webclientActions.NotificationAction.generate(
                    "Login failed with username or password.", "error"))

        return 'success', replyActions
