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
# Date:         12/08/22 2:17 PM
# Project:      djangoPlugin
# Module Name:  fields
# ****************************************************************
from django_zibanu.utils import get_user_object
from rest_framework.serializers import CurrentUserDefault as SourceCurrentUserDefault
from typing import Any


class CurrentUserDefault(SourceCurrentUserDefault):
    """
    Override default class to convert user from TokenUser
    """
    def __call__(self, serializer_field) -> Any:
        """
        Default call method
        :param serializer_field: field received from serializer
        :return:
        """
        local_user = None
        if "request" in serializer_field.context.keys():
            local_user = get_user_object(serializer_field.context.get("request").user)
        return local_user


