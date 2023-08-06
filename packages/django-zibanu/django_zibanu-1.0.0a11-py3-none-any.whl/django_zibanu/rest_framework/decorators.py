# -*- coding: utf-8 -*-

#      Copyright (C)  2022. CQ Inversiones SAS.
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         10/08/22 3:50 PM
# Project:      djangoPlugin
# Module Name:  decorators
# ****************************************************************
from django_zibanu.utils import get_user_object
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def permission_required(perm, raise_exception=True):
    """
    Decorator to validate permissions from django auth structure, including JWT authentication
    :param perm: permission string or tuple with permissions list.
    :param raise_exception: True if you want to raise exception (default), False if not.
    :return: True if successfully
    """
    def check_perms(user):
        """
        Internal function to check perms from master function
        :param user: User object received.
        :return: True if success, False otherwise.
        """
        b_return = False
        local_user = get_user_object(user)

        # Build perms list
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm

        if local_user.has_perms(perms) or local_user.is_superuser:
            b_return = True
        elif raise_exception:
            raise PermissionDenied
        return b_return
    return user_passes_test(check_perms)
