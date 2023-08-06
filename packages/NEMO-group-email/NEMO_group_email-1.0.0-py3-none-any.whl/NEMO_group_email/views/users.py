from NEMO.decorators import staff_member_required
from NEMO.forms import UserForm
from NEMO.models import User
from NEMO.views import users as users_views
from django.contrib.auth.models import Group
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from NEMO_group_email.forms import UserGroupsForm
from NEMO_group_email.utils import render_combine_responses


@staff_member_required
@require_http_methods(["GET", "POST"])
def create_or_modify_user(request, user_id):
    user_groups_dictionary = {
        "groups": Group.objects.all(),
        "user_groups": Group.objects.filter(user=user_id),
    }
    original_response = users_views.create_or_modify_user(request, user_id)

    if request.method == "GET":
        return render_combine_responses(
            request,
            original_response,
            "NEMO_group_email/user_groups.html",
            user_groups_dictionary,
        )
    elif request.method == "POST":
        user = User.objects.get(id=user_id)
        user_form = UserForm(request.POST, instance=user)
        user_group_form = UserGroupsForm(request.POST, instance=user)

        if user_form.is_valid() and user_group_form.is_valid():
            if isinstance(original_response, HttpResponseRedirectBase):
                # It's a redirect, that means everything went ok, save the
                # corresponding user details.
                user_group_form.instance.user = User.objects.get(
                    username=user_form.cleaned_data["username"]
                )
                user_group_form.save()
                return original_response
            else:
                # There was an error and user was not saved, render original combined
                # with details.
                return render_combine_responses(
                    request,
                    original_response,
                    "NEMO_group_email/user_groups.html",
                    user_groups_dictionary,
                )
        else:  # Forms are not valid.
            return render_combine_responses(
                request,
                original_response,
                "NEMO_group_email/user_groups.html",
                user_groups_dictionary,
            )
