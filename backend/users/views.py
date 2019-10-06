from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, RoleSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth import get_user_model
#from rest_framework import jwt, jwt_payload_handler
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
import warnings
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
from . import models 
from drf_writable_nested import WritableNestedModelSerializer
from django.db.models import Avg, Count, Min, Sum, Q
from rest_framework.authtoken.models import Token
import logging

# Create your views here.
class CreateUserAPIView(ListCreateAPIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
    lookup_url_kwarg = 'id'
    serializer_class = UserSerializer
 
    ##def post(self, request):
    ##    user = request.data

        

        #print(user)
    ##    user['password']=make_password(user['password'])

        #user['rolename']=rserializer.data
        
    ##    serializer = UserSerializer(data=user)
    ##    serializer.is_valid(raise_exception=True)
    ##    serializer.save()
    ##    return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        rn=self.request.data['role_key']
        role=models.Role.objects.get(role_key=rn)
        password = make_password(self.request.data['password'])
        serializer.save(role_key=role, password=password)
    '''
    def get_queryset(self):
        #sort = self.kwargs['sort']
        sort = self.request.GET.get('sort','username')
        pipe=sort.find('|')
        order=''
        if pipe > 0:
            order=sort[pipe+1:]
            sort=sort[0:pipe]

            if order.lower()=='desc':
                sort='-' + sort

        else:
            sort='username'

        
        '' '
        sort = request.GET.get('sort','username')
        pipe=sort.find('|')
        order=''
        if pipe > 0:
            order=sort[pipe+1:]
            sort=sort[0:pipe]

            if order.lower()=='desc':
                sort='-' + sort

        else:
            sort='username'
        #print (sort + " " + order)
        User = get_user_model()
        queryset = User.objects.all().order_by(sort)
        
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

        '' '




        return User.objects.all().order_by(sort)
    '''

    def list(self, request):
        '''
        sort = request.GET.get('sort','username')
        pipe=sort.find('|')
        order=''
        if pipe > 0:
            order=sort[pipe+1:]
            sort=sort[0:pipe]

            if order.lower()=='desc':
                sort='-' + sort

        else:
            sort='username'
        #print (sort + " " + order)
        User = get_user_model()
        queryset = User.objects.all().order_by(sort)
        
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
'''


        logger = logging.getLogger('restapi.users')
        logger.info('User listing')

        user=request.user
        #logger.info('user:')
        #logger.info(user)
        urole=user.role_key

        #logger.info('role')
        #logger.debug(userrole)
        #print('search role')
        #print(urole.role_key)
        userrole=urole.role_key

        search=request.GET.get('search','')
        
        role=request.GET.get('role','')

        activeStatus1=request.GET.get('act_1','')
        activeStatus0=request.GET.get('act_0','')


        #export = request.GET.get('export','')
        currentPage= request.GET.get('page','1')
        resultsPerPage = request.GET.get('limit','')
        sort= request.GET.get('sort','-first_name')




        act1=0
        if '' != activeStatus1:
            if activeStatus1=='true':
                act1=1
            else:
                act1=0

        act0=0
        if '' != activeStatus0:
            if activeStatus0=='true':
                act0=1
            else:
                act0=0


        rol=-1
        if role != '':
            rol = int(role)

        User = get_user_model()

        #queryset=search_queryset(fromDate=startdate, toDate=enddate,search=search, is1=act1, is0=act0, ps1=pay1, ps2=pay2, ps3=pay3, relatedUser=prom, sessionProfile=userrole, fromDateP=startdatep, toDateP=enddatep, fromDateC=startdatec, toDateC=enddatec)
        queryset = User.objects.all()

        if act1 > 0 or act0 > 0:
                q_act = Q()

                if act1 > 0:
                    q_act |= Q(is_active = True)

                if act0 > 0:
                    q_act |= Q(is_active = False)

                queryset = queryset.filter( q_act )

        if search != '':
                q_search = Q()

                q_search |= Q(firstname__icontains = search)
                q_search |= Q(lastname__icontains = search)
                q_search |= Q(username__icontains = search)

                queryset = queryset.filter( q_search )
        #page = int(currentPage)
        #perpage = int(resultsPerPage)
        #offset=0
        #offset = (page -1) * perpage
        #total = 0
        #total = perpage
        #total = total + offset

        #queryset=queryset.order_by(sort)[offset:total]



        page = int(currentPage)
        perpage = int(resultsPerPage)
        offset=0
        offset = (page -1) * perpage
        total = 0
        total = perpage
        total = total + offset
        queryset = queryset.order_by(sort)[offset:total]
            
        logger.info(queryset.query)
        serializer = UserSerializer(queryset, many=True)
        
        return Response(serializer.data)

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

class UserRetrieveUpdateAPIView(UpdateAPIView):
 
    # Allow only authenticated users to access this url
    #permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = models.User.objects.all()
    permission_classes = (AllowAny,)
    lookup_field = ('id')
    #response = view(request, pk=1)
   
 
    ###def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        ###serializer = self.serializer_class(request.user)
 
        ###return Response(serializer.data, status=status.HTTP_200_OK)
 
    def put(self, request, *args, **kwargs):
        #serializer_data = request.data.get('user', {})
        id = self.kwargs['id']

        u=models.User.objects.get(pk=id)
        #r=models.Role.object.get(role_name=data['rolename'])
        data=request.data

        if data['password'] !='' :
            data['password'] = make_password(data['password'])
        else:
            data['password'] = u.password

        #data['rolename'] = r

        serializer=UserSerializer(u, data=data)
        #print("antes valid " + data['rolename'] + ' ' + u.rolename.role_name)
        if serializer.is_valid():
            print("valid")
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #User = get_user_model()
        #queryset = models.User.objects.all().filter(id=id)
 
        ###instance = self.get_object()
        #print(request.data)
        #serializer = UserSerializer(self, data=request.data, partial=True, many=False)
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
        #return Response(serializer.data)

        #serializer = UserSerializer(
        #    request.user, data=serializer_data, partial=True
        #)
        
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
 
        return Response('ok', status=status.HTTP_200_OK)

class UserListingAPIView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = UserSerializer

    def list(self, request):
        sort = request.GET.get('sort','username')
        pipe=sort.find('|')
        order=''
        if pipe > 0:
            order=sort[pipe+1:]
            sort=sort[0:pipe]

            if order.lower()=='desc':
                sort='-' + sort

        else:
            sort='username'
        #print (sort + " " + order)
        User = get_user_model()
        queryset = User.objects.all().order_by(sort)
        
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class UserPromotorAPIView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    queryset = models.User.objects.all()

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = UserSerializer

    def list(self, request):
        User = get_user_model()
        #(Q(fac_receptorrfc__icontains=search)| Q(fac_folio__icontains=search)| Q(fac_receptornombre__icontains=search) | Q(fac_xml__icontains=search) )
        queryset = User.objects.all().filter(Q(role_key=3) | Q( role_key=5)).order_by('first_name', 'last_name')
        
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class RoleAPIView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    queryset = models.Role.objects.all()

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = RoleSerializer

    def list(self, request):
        #Role = models.Role()
        queryset = models.Role.objects.all()
        
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data)

'''
    def get(self, request, *args, **kwargs):

        User = get_user_model()
        
        user=User.objects.all()

        serializer = UserSerializer(data=user, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
'''
class Logout(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        # simply delete the token to force a login
        #if request.user :
        #    request.user.auth_token.delete()
        
        return Response(status=status.HTTP_200_OK)

class UserInfoAPIView(APIView):
    #permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated,)
    
    serializer_class=UserSerializer
    def get(self, request, *args, **kwargs):

        logger = logging.getLogger('restapi.users')

        User =  get_user_model()
        id = request.user.id 

        #id= self.kwargs['id']
        queryset=User.objects.get(id=id)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserSingleAPIView(APIView):
    permission_classes = (AllowAny,)

    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        id = self.kwargs['id']

        queryset = User.objects.get(id=id)

        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user).data
    }
