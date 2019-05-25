from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import InvoiceSerializer, InvoiceNoXmlSerializer, InvoiceLogSerializer, InvoiceReminderSerializer, InvoicePaymentHistorySerializer #, PromotorPieSerializer
from django.core import serializers
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
from .models import Invoice, InvoiceLog, InvoiceReminders, InvoicePaymentHistory
from django.db.models import Avg, Count, Min, Sum, Q
from datetime import datetime, timedelta
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
import logging
from rest_framework.authtoken.models import Token
from users.models import User, Role

# Create your views here.

class UpdateInvoiceAPIView(UpdateAPIView):
    permission_classes = (AllowAny,)

    def put(self, request,*args,**kwargs):
        id = self.kwargs['id']
        logger = logging.getLogger('restapi.invoices')
        i=Invoice.objects.get(pk=id)
        data=request.data
        logger.debug(data)
        #print(data)

        serializer=InvoiceSerializer(i,data=data)
        #logger.debug(serializer.initial_data['fac_pagada'])
        if serializer.is_valid():
            logger.debug('antes save update')
            print('antes save update')
            #print(serializer.validated_data['fac_isactive'])
            #logger.debug(serializer.validated_data['fac_pagada'])
            serializer.save(raise_exception=True)
            logger.debug(serializer.data['fac_isactive'])
            print(serializer.data['fac_isactive'])
            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class NewInvoiceAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
 
    def post(self, request):
        return Response(request.data, status=status.HTTP_201_CREATED)
'''
        invoice = request.data
        #print(user)
        user['password']=make_password(user['password'])
        serializer = InvoiceSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''

class MissingInvoiceAPIView(APIView):
 
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)
        i=Invoice()
        rows=i.missing_invoices()

        return Response(json.dumps(rows), status=status.HTTP_200_OK)

class InvoiceSingleAPIView(APIView):
    permission_classes = (AllowAny,)

    serializer_class = InvoiceSerializer
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        print(id)
        queryset = Invoice.objects.get(fac_key=id)
        
        serializer = InvoiceSerializer(queryset)
        
        return Response(serializer.data, status=status.HTTP_200_OK)




class InvoiceListingAPIView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (IsAuthenticated,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = InvoiceNoXmlSerializer

    def list2(self, request):
        queryset = Invoice.objects.all().defer('fac_xml').filter(fac_fecha__gte=date.today() - timedelta(days=30)).order_by('-fac_fecha', 'fac_serie', 'fac_folio')[:10]
        
        serializer = InvoiceNoXmlSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def search_queryset(self, fromDate, toDate, search, invoiceStatus, paymentStatus, relatedUser, sessionProfile):

        queryset = Invoice.objects.all()

        # Specific search for Promotors
        if sessionProfile == 3 :
            queryset = queryset.filter(fac_isactive= True, fac_pagada=2, fac_iduser=relatedUser)
        else:
            if relatedUser != 0 :
                queryset = queryset.filter(fac_iduser = relatedUser)




        return queryset
    


    def list(self, request):
        #user = Token.objects.get(key='token string').user

        logger = logging.getLogger('restapi.invoices')
        logger.info('Invoice listing')

        user=request.user
        userrole=user.role_key
        logger.info('role')
        logger.info(userrole)

        sort = request.GET.get('sort','-fac_fecha')
        #pipe=sort.find('+')
        ##order=''
        #isprom=request.GET.get('isprom','')
        #if pipe > 0:
        #    order=sort[pipe+1:]
        #   sort=sort[1:]

        ##  if order.lower()=='desc':
        ##        sort='-' + sort

        ##else:
        ##    sort='-fac_fecha'

        logger.info('sort')
        logger.info(sort)

        #page = request.GET.get('page', '1')
        page=1
        #perpage= request.GET.get('per_page','50')
        perpage=10
        offset=(int(page)-1) * int(page)
        total=int(perpage)*1
        total=total+offset


        search=request.GET.get('search','')
        fromd=request.GET.get('from','')
        tod=request.GET.get('to','')
        promotorid=request.GET.get('promotorid','')
        paid=request.GET.get('fac_pagada','')

        logger.info('search terms: search: ' + search + ', fromd: ' + fromd + ', tod: ' + tod + ', promotorid: ' + promotorid + ', paid: ' + paid)

        startdate=None
        enddate=None
        isp=False

        pid=0
        if '' != promotorid:
            pid=int(promotorid)

        

        if 3 == userrole.role_key :
            isp=True
            logger.info('User is promotor')

        #queryset = Invoice.objects.all()
        queryset = self.search_queryset(fromDate=None, toDate=None, search='', invoiceStatus=0, paymentStatus=2, sessionProfile=userrole, relatedUser=0 )
        #queryset = queryset.filter(fac_isactive=True)
        if(True==isp):
            queryset=queryset.filter(Q(fac_pagada=2))
            logger.info('Lookup fac_pagada=2')
        else:

        #if 1 != userrole.role_key :
        #    queryset=queryset.filter( ~Q(fac_pagada =3) )

            if '' != paid and 'true' == paid:
                queryset=queryset.filter( Q(fac_pagada=1) | Q(fac_pagada=2) | Q(fac_pagada=3))
                logger.info('Lookup fac_pagada=1 or 2 or 3')
            else:
                queryset=queryset.filter( ~Q(fac_pagada=1) )
                logger.info('Lookup fac_pagada != 1')

        if pid > 0:
            queryset = queryset.filter(fac_iduser=pid)
            logger.info('Lookup fac_iduser=pid')
            #if True == isp:
                #queryset=queryset.filter( ~Q(fac_pagada =3) & ~Q(fac_pagada=1))

        if '' != search:
            queryset=queryset.filter(Q(fac_receptorrfc__icontains=search)| Q(fac_folio__icontains=search)| Q(fac_receptornombre__icontains=search) )
            logger.info('Lookup search text: ' + search)

        q_dates = Q()
        if '' != fromd:
            startdate = datetime.strptime(fromd, '%Y-%m-%d')
        if '' != tod:
            enddate = datetime.strptime(tod, '%Y-%m-%d') + timedelta(minutes=1439)

        #logger.debug(enddate)
        

        if startdate != None and enddate != None:
            q_dates &= Q(fac_fecha__gte=startdate) 
            q_dates &= Q(fac_fecha__lte=enddate)
            queryset = queryset.filter(q_dates)
            logger.info('Lookup between dates')
        
        elif startdate == None and enddate != None:
            q_dates=Q(fac_fecha__lte=enddate)
            logger.info('Lookup less than enddate' + str(enddate) )

        elif enddate == None and startdate != None :
            q_dates=Q(fac_fecha__gte=startdate)
            logger.info('Lookup more than startdate' + str(startdate) )
        
        #tags = ['tag1', 'tag2', 'tag3']
        #q_objects = Q() # Create an empty Q object to start with
        #for t in tags:
        #q_objects |= Q(tags__tag__contains=t)
        #.filter(q_objects)
        #queryset = Invoice.objects.all()

        #if q_dates:
        #    queryset = queryset.filter(q_dates) #order_by(sort)[offset:total]
        
        #logger.debug(queryset.query)
        #print (queryset.query)
        
        queryset=queryset.order_by(sort)[offset:total]
        serializer = InvoiceNoXmlSerializer(queryset, many=True)
        
        return Response(serializer.data)


class InvoicePromotorPieAPIView(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    #serializer_class = PromotorPieSerializer(, many=True)

    def get(self, request, *args, **kwargs):
        fromDate = request.GET.get('from')
        toDate = request.GET.get('to')
        
        i=Invoice()
        rows=i.promotor_pie_data(fromDate,toDate)
        data = serializers.serialize("json",rows)

        #serializer = PromotorPieSerializer(rows, many=True)


        return Response( data, status=status.HTTP_200_OK)
class InvoiceDebtAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)

        #fromDate = datetime.strptime(request.GET.get('from'),'%Y-%m-%d')
        #toDate = datetime.strptime(request.GET.get('to'),'%Y-%m-%d')

        i=Invoice.objects.filter(Q(fac_pagada=2) & Q(fac_isactive=True)).aggregate(s=Sum('fac_total'))
        income=i['s']
        if None == income:
            result=0
        else:
            result=income
        return Response(json.dumps(result), status=status.HTTP_200_OK)


class InvoiceIncomeAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)
    
        fromDate = datetime.strptime(request.GET.get('from'),'%Y-%m-%d')
        toDate = datetime.strptime(request.GET.get('to'),'%Y-%m-%d')

        i=Invoice.objects.filter(fac_fechapago__gte=fromDate, fac_fechapago__lte=toDate+timedelta(minutes=1439), fac_pagada=1, fac_isactive=True).aggregate(s=Sum('fac_total'))
        income=i['s']
        if None == income:
            result=0
        else:
            result=income
        return Response(json.dumps(result), status=status.HTTP_200_OK)

class InvoiceCountAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)
    
        fromDate = datetime.strptime(request.GET.get('from'),'%Y-%m-%d')
        toDate = datetime.strptime(request.GET.get('to'),'%Y-%m-%d')

        i=Invoice.objects.filter(fac_cdate__gte=fromDate, fac_cdate__lte=toDate+timedelta(minutes=1439)).count()
        #print(i)
        #income=i['fac_total']
        if None == i:
            result=0
        else:
            result=i
        return Response(json.dumps(result), status=status.HTTP_200_OK)

class FirstUnpaidDateAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)
    
        #fromDate = request.GET.get('from')
        #toDate = request.GET.get('to')

        #i=Invoice.objects.filter(fac_fechapago__range=[fromDate, toDate]).count()
        i=Invoice.objects.filter(fac_pagada=2, fac_isactive=True).aggregate(Min('fac_fecha'))

        #print(i)
        
        if None == i:
            result=0
        else:
            d=i['fac_fecha__min']
            #f = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
            result= d.strftime("%Y-%m-%d")
        return Response(json.dumps(result), status=status.HTTP_200_OK)

class FirstUnpaidInvoiceAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)
    
        #fromDate = request.GET.get('from')
        #toDate = request.GET.get('to')

        #i=Invoice.objects.filter(fac_fechapago__range=[fromDate, toDate]).count()
        i=Invoice.objects.filter(fac_pagada=2, fac_isactive=True).aggregate(Min('fac_fecha'))

        #print(i)
        
        if None == i:
            result=''
        else:
            d=i['fac_fecha__min']
            i2=Invoice.objects.filter(fac_pagada=2, fac_isactive=True, fac_fecha=d).order_by('fac_fecha').first()

            if None == i2:
                result=''
            else:
                result= i2.fac_serie + ' ' + str(i2.fac_folio)
        return Response(json.dumps(result), status=status.HTTP_200_OK)

class InvoiceLogListingAPIView(APIView):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = InvoiceLogSerializer

    def get(self, requesti,*args,**kwargs):
        id = self.kwargs['id']
        queryset = InvoiceLog.objects.all().filter(log_invoice=int(id)).order_by('-log_datetime')
        
        serializer = InvoiceLogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InvoiceReminderListingAPIView(APIView):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = InvoiceReminderSerializer

    def get(self, request,*args,**kwargs):
        id = self.kwargs['id']
        queryset = InvoiceReminders.objects.all().filter(rem_invoice=id).order_by('-rem_datetime')
        
        serializer = InvoiceReminderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InvoicePaymentHistoryListingAPIView(APIView):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = InvoicePaymentHistorySerializer

    def get(self, request,*args,**kwargs):
        id = self.kwargs['id']
        queryset = InvoicePaymentHistory.objects.all().filter(his_invoice=id).order_by('-his_date')
        
        serializer = InvoicePaymentHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InvoiceUpload(APIView):
    parser_class=(FileUploadParser,)
    permission_classes = (AllowAny,)

    def put(self,request,*args,**kwargs):
        if 'file' not in request.data:
            raise ParserError("Empty content")

        f=request.data['file']
        #print(f)
        i=Invoice()
        i.upload(f)

        return Response(status=status.HTTP_201_CREATED)


class NewInvoiceLog(APIView):
    permission_classes = (AllowAny, )

    def post(self,request):
        logdata=request.data
        serializer= InvoiceLogSerializer(data=logdata)
        serializer.is_valid(raise_exception=True)
        l=serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NewInvoiceReminder(APIView):
    permission_classes = (AllowAny, )

    def post(self,request):
        remdata=request.data
        rd=remdata['rem_datetime']
        #print(rd)
        fd=datetime.strptime(rd, '%Y-%m-%d')#.date() + timedelta(hours=12)
        #print(fd)
        remdata['rem_datetime']=fd#.strftime("YYYY-MM-DDThh:mm:ss")
        #print(remdata['rem_datetime'])
        serializer= InvoiceReminderSerializer(data=remdata)
        serializer.is_valid(raise_exception=True)
        l=serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewInvoicePaymentHistory(APIView):
    permission_classes = (AllowAny, )

    def post(self,request):
        paydata=request.data
        serializer= InvoicePaymentHistorySerializer(data=paydata)
        serializer.is_valid(raise_exception=True)
        l=serializer.save()

        inv=request.data['his_invoice']

        #ph=InvoicePaymentHistory()
        paid=InvoicePaymentHistory.objects.get_sum_payments(id=inv)
        print(paid)
        i=Invoice.objects.get(pk=inv)
        i.fac_payments=paid
        i.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': InvoiceSerializer(user).data
    }
