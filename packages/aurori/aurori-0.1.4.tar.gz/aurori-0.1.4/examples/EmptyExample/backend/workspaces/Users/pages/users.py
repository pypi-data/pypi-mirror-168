from aurori.workspaces import Page
""" The log page
"""


class Users(Page):
    title = 'Users'  # Shown label of the page in the menu
    group = 'Admin'  # groupname multiple pages
    icon = 'supervisor_account'  # icon (in typeset of material design icons)
    route = '/admin/users'  # routing
    builder = 'frontend'  # page get build by the client (frontend)
    rank = 3.0  # ranks (double) the page higher values are at the top of the menu
    # groups will be ranked by the sum of the rank-values of their entries
    requireLogin = True  # login is required to view the page
