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
# Date:         10/08/22 4:48 PM
# Project:      djangoPlugin
# Module Name:  viewsets
# ****************************************************************
from django.conf import settings
from django.db import DatabaseError
from django_zibanu.rest_framework.exceptions import APIException
from django_zibanu.lib.messages import ErrorMessages
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet as SourceViewSet
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class ModelViewSet(SourceViewSet):
    """
    Override vlass ModelViewSet to load default permissions and other features
    """
    http_method_names = ["post"]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    if settings.DEBUG:
        # If DEBUG, allow TokenAuthentication to run ViewSet
        authentication_classes.append(authentication.TokenAuthentication)

    def list(self, request, *args, **kwargs):
        """
        Base method to list the items from model
        :param request: request object received from HTTP
        :param args: args data from request
        :param kwargs: kwargs data from request
        :return:
        """
        try:
            serializer = self.get_serializer(instance=self.get_queryset(), many=True)
            data_return = serializer.data
            status_return = status.HTTP_200_OK if len(data_return) > 0 else status.HTTP_204_NO_CONTENT
        except APIException as exc:
            raise APIException(msg=exc.detail.get("message"), error=exc.detail.get("detail"),
                               http_status=exc.status_code) from exc
        except Exception as exc:
            raise APIException(error=str(exc), http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=data_return, status=status_return)

    def create(self, request, *args, **kwargs):
        """
        Base method to create an instance of entity
        :param request: request object received from HTTP
        :param args: args data from request
        :param kwargs: kwargs data from request
        :return:
        """
        try:
            data_return = []
            status_return = status.HTTP_400_BAD_REQUEST
            request_data = request.data
            if len(request_data) > 0:
                serializer = self.get_serializer(data=request_data)
                if serializer.is_valid(raise_exception=True):
                    created = serializer.create(validated_data=serializer.validated_data)
                    if created is not None:
                        data_return = self.get_serializer(created).data
                        status_return = status.HTTP_201_CREATED
                    else:
                        raise ValidationError(ErrorMessages.CREATE_ERROR, "create")
            else:
                raise APIException(ErrorMessages.DATA_REQUIRED)
        except DatabaseError as exc:
            raise APIException(ErrorMessages.DATABASE_ERROR, str(exc)) from exc
        except ValidationError as exc:
            raise APIException(error=str(exc.detail), http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except APIException as exc:
            raise APIException(exc.detail.get("message"), exc.detail.get("detail"), exc.status_code) from exc
        except Exception as exc:
            raise APIException(error=str(exc), http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status_return, data=data_return)


