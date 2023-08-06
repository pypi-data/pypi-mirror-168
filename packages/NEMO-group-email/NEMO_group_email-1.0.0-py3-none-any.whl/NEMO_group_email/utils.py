"""
"""
import importlib
from functools import wraps

from django.http import HttpResponse
from django.shortcuts import render


def render_combine_responses(
    request, original_response: HttpResponse, template_name, context
):
    """Combines contents of an original http response with a new one"""
    additional_content = render(request, template_name, context)
    original_response.content += additional_content.content
    return original_response


def replace_function(old_function_name):
    pkg, fun_name = old_function_name.rsplit(".", 1)
    pkg_mod = importlib.import_module(pkg)
    old_function = getattr(pkg_mod, fun_name)

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(old_function, *args, **kwargs)

        setattr(pkg_mod, fun_name, wrapper)
        return wrapper

    return decorator
