from aurori.workspaces import Page

from workspaces.Log.permissions import ViewLogs

""" The log page
"""


class Log(Page):
    title = "Log"  # Shown label of the page in the menu
    group = "Admin"  # groupname multiple pages
    icon = "description"  # icon (in typeset of material design icons)
    route = "/admin/log"  # routing
    builder = "frontend"  # page get build by the client (frontend)
    rank = 0.1  # ranks (double) the page higher values are at the top of the menu
    # groups will be ranked by the sum of the rank-values of their entries
    requireLogin = True  # login is required to view the page
    requirePermission = ViewLogs()
    requireAdmin = False  # login dont need admin privileges
