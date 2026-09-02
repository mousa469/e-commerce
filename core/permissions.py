from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from core.constants import ADMIN_ROLE , CLIENT_ROLE


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        return request.user.role == ADMIN_ROLE




class IsClient(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        return request.user.role ==  CLIENT_ROLE



class ReviewOwner(IsClient):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) :
         return request.user == obj.user
