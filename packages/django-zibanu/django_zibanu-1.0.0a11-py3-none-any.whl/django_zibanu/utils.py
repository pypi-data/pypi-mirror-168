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

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         12/08/22 2:28 PM
# Project:      djangoPlugin
# Module Name:  utils
# ****************************************************************
from django.contrib import auth
from rest_framework_simplejwt.models import TokenUser
from typing import Any


def get_user_object(user: Any) -> Any:
    """
    Function to get User objecto from TokenUser or another object.
    :param user: Any: User object to be converted
    :return: User: User object.
    """
    local_user = user
    user_model = auth.get_user_model()
    if isinstance(user, TokenUser):
        local_user = user_model.objects.get(pk=local_user.id)

    return local_user
