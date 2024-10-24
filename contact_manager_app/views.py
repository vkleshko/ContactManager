import json
import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contact_manager_app.models import Contact
from contact_manager_app.serializers import (
    ContactSerializer,
    ContactCreateSerializer,
    ContactDetailSerializer,
)


class ContactListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_contact(id):
        return get_object_or_404(Contact, id=id)

    def get(self, request, id):
        contact = self.get_contact(id)
        serializer = ContactDetailSerializer(contact)

        return Response(serializer.data)

    def put(self, request, id):
        contact = self.get_contact(id)
        serializer = ContactCreateSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        contact = self.get_contact(id)
        contact.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name="dispatch")
class ConvertTokenView(View):
    def post(self, request):
        data = json.loads(request.body)
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")
        token = data.get("token")

        payload = {
            "client_id": client_id,
            "grant_type": "convert_token",
            "client_secret": client_secret,
            "backend": "google-oauth2",
            "token": token,
        }

        url = "http://127.0.0.1:8000/auth/convert-token/"
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            user = response.json().get("user", {})

            contact_data = {
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "email": user.get("email"),
            }
            serializer = ContactCreateSerializer(data=contact_data)
            if serializer.is_valid():
                serializer.save()

            return JsonResponse(response.json(), status=status.HTTP_200_OK)

        return JsonResponse(response.json(), status=status.HTTP_400_BAD_REQUEST)
