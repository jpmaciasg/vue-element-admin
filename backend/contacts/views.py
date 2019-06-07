from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ContactSerializer, ContactUserSerializer,ContactListSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
#from rest_framework import jwt, jwt_payload_handler
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
import warnings
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
#from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
import simplejson as json
from .models import Contact
from django.db.models import Avg, Count, Min, Sum
from . import models
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
import logging

# Create your views here.

class NewContactAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
 
    def post(self, request):
        contact = request.data
        #print(contact)
        serializer = ContactSerializer(data=contact)
        serializer.is_valid(raise_exception=True)
        c=serializer.save()

        u= models.User(pk=contact['cu_id'])
        r=ContactUser(cu_contact_id=c, cu_id=u)
    
        r.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateContactAPIView(UpdateAPIView):
    permission_classes = (AllowAny,)

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        logger = logging.getLogger('restapi.contacts')
        i = Contact.objects.get(pk=id)
        data = request.data
        #logger.debug(data)
        #print(data)

        serializer = ContactSerializer(i, data=data)
        #logger.debug(serializer.initial_data['fac_pagada'])
        if serializer.is_valid():
            #logger.debug('antes save update')
            #print('antes save update')
            #print(serializer.validated_data['fac_isactive'])
            #logger.debug(serializer.validated_data['fac_pagada'])
            serializer.save(raise_exception=True)
            #logger.debug(serializer.data['fac_isactive'])
            #print(serializer.data['fac_isactive'])
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
class AuthUserAPIView(APIView):
    # @api_view(['POST'])
    # @permission_classes((AllowAny,))
    permission_classes = (AllowAny,)
    def post(self, request):
        
        try:
            #email = request.data['email']
            username = request.data['username']
            password = request.data['password']
            
            User = get_user_model()
    
            user = User.objects.get(username=username, password=password)
            if user:
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['name'] = "%s %s" % (
                        user.first_name, user.last_name)
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
    
                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a username and a password'}
            return Response(res)
'''
class ContactSingleAPIView(APIView):
    permission_classes = (AllowAny,)

    serializer_class = ContactSerializer
    def get(self, request, *args, **kwargs):
        
        id = self.kwargs['id']


        #queryset = models.Contact.objects.all().values('id','contact_fullname','contact_type','contact_email','contact_phone','contact_taxid','contact_byname','contactuser__id','contactuser__cu_contact_id','contactuser__cu_id','contactuser__cu_id__username','contactuser__cu_id__id').filter(id=id)
        queryset = Contact.objects.get(id=id)

        serializer = ContactSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContactListingAPIView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = ContactSerializer

    def list(self, request):
        sort = request.GET.get('sort','contact_fullname')
        pipe=sort.find('|')
        order=''
        if pipe > 0:
            order=sort[pipe+1:]
            sort=sort[0:pipe]

            if order.lower()=='desc':
                sort='-' + sort

        else:
            sort='contact_fullname'

        #queryset= ContactUser.objetcts.all()
        queryset = Contact.objects.all().values('id','contact_fullname','contact_type','contact_email','contact_phone','contact_taxid','contact_byname','contactuser__id','contactuser__cu_contact_id','contactuser__cu_id','contactuser__cu_id__username','contactuser__cu_id__id').order_by(sort)[:100]
        #Employee.objects.all().values('id','name','company__name')
        #print(queryset)
        serializer = ContactListSerializer(queryset, many=True)
        return Response(serializer.data)
'''
    def get(self, request, *args, **kwargs):

        User = get_user_model()
        
        user=User.objects.all()[:100]

        serializer = InvoiceSerializer(data=user, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
'''

class ContactCountContactAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)

        i=Contact.objects.count()

        if None == i:
            result=0
        else:
            result=i
        return Response(json.dumps(result), status=status.HTTP_200_OK)

class ContactCountClientAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)
        
        i=Contact.objects.exclude(contact_taxid__isnull=True).count()
        #print(i)
        #income=i['fac_total']
        if None == i:
            result=0
        else:
            result=i
        return Response(json.dumps(result), status=status.HTTP_200_OK)


