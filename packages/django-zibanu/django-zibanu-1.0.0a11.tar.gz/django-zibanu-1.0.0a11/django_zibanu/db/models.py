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
# Date:         27/08/22 3:12 PM
# Project:      djangoPlugin
# Module Name:  models
# ****************************************************************
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Base class to create new models with standard fields and save.
    """
    # Validations errors.
    validation_messages = {
        "field_required": _("Error! The field %s is required.")
    }

    class Meta:
        """
        META class for BaseModel
        """
        abstract = True


class DatedModel(BaseModel):
    created_at = models.DateTimeField(blank=False, null=False, verbose_name=_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(blank=False, null=False, verbose_name=_("Modified at"), auto_now=True)

    class Meta:
        """
        META class for DatedModel
        """
        abstract = True

