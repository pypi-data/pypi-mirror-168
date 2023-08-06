from NEMO.models import User
from django.forms import ModelForm


class UserGroupsForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "groups",
        ]
