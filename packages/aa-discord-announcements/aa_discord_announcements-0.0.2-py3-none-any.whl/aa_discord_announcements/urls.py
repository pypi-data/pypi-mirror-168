"""
Pages url config
"""

# Django
from django.urls import include, path

# AA Discord Announcements
from aa_discord_announcements import views

app_name: str = "aa_discord_announcements"

urlpatterns = [
    path(route="", view=views.index, name="index"),
    # Ajax calls
    path(
        route="ajax/",
        view=include(
            [
                path(
                    route="get-announcement-targets-for-user/",
                    view=views.ajax_get_announcement_targets,
                    name="ajax_get_announcement_targets",
                ),
                path(
                    route="get-webhooks-for-user/",
                    view=views.ajax_get_webhooks,
                    name="ajax_get_webhooks",
                ),
                path(
                    route="create-announcement/",
                    view=views.ajax_create_announcement,
                    name="ajax_create_announcement",
                ),
            ]
        ),
    ),
]
