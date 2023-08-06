from django.conf.urls import url

from NEMO_group_email.views import email, users

urlpatterns = [
    url(r"^email_broadcast/$", email.email_broadcast, name="email_broadcast"),
    url(
        r"^email_broadcast/(?P<audience>tool|area|account|project|user|group)/$",
        email.email_broadcast,
        name="email_broadcast",
    ),
    url(
        r"^user/(?P<user_id>\d+|new)/",
        users.create_or_modify_user,
        name="create_or_modify_user",
    ),
]
