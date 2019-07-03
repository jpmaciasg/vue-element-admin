from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import InvoiceSerializer, InvoiceNoXmlSerializer, InvoiceLogSerializer, InvoiceReminderSerializer, InvoicePaymentHistorySerializer,InvoiceEdHistorySerializer #, PromotorPieSerializer
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
from rest_framework.pagination import PageNumberPagination
import simplejson as json
from .models import Invoice, InvoiceLog, InvoiceReminders, InvoicePaymentHistory, InvoiceEdHistory
from django.db.models import Avg, Count, Min, Sum, Q
from datetime import datetime, timedelta
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
import logging
from rest_framework.authtoken.models import Token
from users.models import User, Role
from .search import search_queryset 
# Create your views here.

class UpdateInvoiceAPIView(UpdateAPIView):
    permission_classes = (AllowAny,)

    def put(self, request,*args,**kwargs):
        id = self.kwargs['id']
        logger = logging.getLogger('restapi.invoices')
        i=Invoice.objects.get(pk=id)
        data=request.data

        ed = data.get('fac_expectedpaymentday','-1') #request.POST.get('fac_expectedpaymentday', '-1')
        #logger.debug(ed)
        #print(ed)
        data2={}
        if '-1' != ed:
            #print('entra')
            user=request.user
            uid=user.id
            #edc=i['fac_edupdatescount']
            #data['fac_edupdatescount']=edc + 1

            data2['ed_invoice']=id
            if i.fac_expectedpaymentday != None:
                data2['ed_olddate']=str(i.fac_expectedpaymentday)+'T00:00:00'
            else:
                data2['ed_olddate']=None #str(i.fac_expectedpaymentday)+'T00:00:00' #.strftime('%Y-%m-%d')
            if data['fac_expectedpaymentday'] != None:
                data2['ed_newdate']= data['fac_expectedpaymentday']+'T00:00:00'
            else:
                data2['ed_newdate']=None #data['fac_expectedpaymentday']+'T00:00:00'
            data2['ed_user']=uid
            #print(data2)

            s2= InvoiceEdHistorySerializer(data=data2)
            #print('creado')
            s2.is_valid(raise_exception=True)
            #print('valido')
            l2=s2.save()
            #print('guardo')

            qs=InvoiceEdHistory.objects.filter(ed_invoice=id).count()
            data['fac_edupdatescount']=qs
            #print('asigno')

        #logger.debug(data)
        #print(data)

        serializer=InvoiceSerializer(i,data=data)
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


    def list(self, request):
        #user = Token.objects.get(key='token string').user

        logger = logging.getLogger('restapi.invoices')
        logger.info('Invoice listing')

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
        fromd=request.GET.get('from','')
        tod=request.GET.get('to','')
        fromdp=request.GET.get('fromp','')
        todp=request.GET.get('top','')
        fromdc=request.GET.get('fromc','')
        todc=request.GET.get('toc','')
        promotor=request.GET.get('promotor','')
        paymentStatus1=request.GET.get('pay_1','')
        paymentStatus2=request.GET.get('pay_2','')
        paymentStatus3=request.GET.get('pay_3','')

        activeStatus1=request.GET.get('act_1','')
        activeStatus0=request.GET.get('act_0','')

        countrows= request.GET.get('countrows','')
        sumrows = request.GET.get('sumrows','')
        payedrows = request.GET.get('payedrows','')

        export = request.GET.get('export','')
        currentPage= request.GET.get('page','1')
        resultsPerPage = request.GET.get('limit','')
        sort= request.GET.get('sort','-fac_fecha')

        startdate=None
        enddate=None
        startdatep=None
        enddatep=None
        startdatec=None
        enddatec=None
        
        if '' != fromd:
            startdate = datetime.strptime(fromd[0:10], '%Y-%m-%d')
        if '' != tod:
            enddate = datetime.strptime(tod[0:10], '%Y-%m-%d') + timedelta(minutes=1439)

        if '' != fromdp:
            startdatep = datetime.strptime(fromdp[0:10], '%Y-%m-%d')
        if '' != todp:
            enddatep = datetime.strptime(todp[0:10], '%Y-%m-%d')

        if '' != fromdc:
            startdatec = datetime.strptime(fromdc[0:10], '%Y-%m-%d')
        if '' != todc:
            enddatec = datetime.strptime(todc[0:10], '%Y-%m-%d')


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

        pay1=0
        if '' != paymentStatus1:
            if paymentStatus1=='true':
                pay1=1
            else:
                pay1=0

        pay2=0
        if '' != paymentStatus2:
            if paymentStatus2=='true':
                pay2=1
            else:
                pay2=0

        pay3=0
        if '' != paymentStatus3:
            if paymentStatus3=='true':
                pay3=1
            else:
                pay3=0

        prom=-1
        if promotor != '':
            prom = int(promotor)

        queryset=search_queryset(fromDate=startdate, toDate=enddate,search=search, is1=act1, is0=act0, ps1=pay1, ps2=pay2, ps3=pay3, relatedUser=prom, sessionProfile=userrole, fromDateP=startdatep, toDateP=enddatep, fromDateC=startdatec, toDateC=enddatec)

        #page = int(currentPage)
        #perpage = int(resultsPerPage)
        #offset=0
        #offset = (page -1) * perpage
        #total = 0
        #total = perpage
        #total = total + offset

        #queryset=queryset.order_by(sort)[offset:total]

        if countrows != '':
            queryset = queryset.count()
            if None == queryset:
                result=0
            else:
                result = queryset

            return Response(json.dumps(result), status=status.HTTP_200_OK)
        elif sumrows != '':
            queryset = queryset.aggregate(s=Sum('fac_total'))
            s= queryset['s']
            if None == s:
                result=0
            else:
                result=s

            return Response(json.dumps(result), status=status.HTTP_200_OK)
        elif payedrows != '':
            queryset = queryset.aggregate(s=Sum('fac_payments'))
            s=queryset['s']
            if None == s:
                result=0
            else:
                result=s
            return Response(json.dumps(result), status = status.HTTP_200_OK)
        else:
            if export != '':
                queryset = queryset.order_by(sort)
            else:
                page = int(currentPage)
                perpage = int(resultsPerPage)
                offset=0
                offset = (page -1) * perpage
                total = 0
                total = perpage
                total = total + offset
                queryset = queryset.order_by(sort)[offset:total]
            
            logger.info(queryset.query)
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
    
        fromd=request.GET.get('from','')
        tod=request.GET.get('to','')

        startdate=None
        enddate=None
       
        if '' != fromd:
            startdate = datetime.strptime(fromd[0:10], '%Y-%m-%d')
        if '' != tod:
            enddate = datetime.strptime(tod[0:10], '%Y-%m-%d') + timedelta(minutes=1439)

        queryset=search_queryset(fromDate=startdate, toDate=enddate,search='', is1=1, is0=0, ps1=1, ps2=0, ps3=0, relatedUser=-1, sessionProfile=0, fromDateP=None, toDateP=None, fromDateC=None, toDateC=None)

        queryset = queryset.aggregate(s=Sum('fac_total'))
        result = queryset['s']
        r=0
        if None == result:
            r =0
        else:
            r = result

        return Response(json.dumps(r), status=status.HTTP_200_OK)
        #i=Invoice.objects.filter(fac_fechapago__gte=fromDate, fac_fechapago__lte=toDate+timedelta(minutes=1439), fac_pagada=1, fac_isactive=True).aggregate(s=Sum('fac_total'))
        #income=i['s']
        #if None == income:
        #    result=0
        #else:
        #    result=income
        #return Response(json.dumps(result), status=status.HTTP_200_OK)

class InvoiceCountAPIView(APIView):
    # Allow only authenticated users to access this url
    permission_classes = (AllowAny,)
    #serializer_class = InvoiceSerializer
 
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        #serializer = self.serializer_class(request.user)
    
        #fromDate = datetime.strptime(request.GET.get('from'),'%Y-%m-%d')
        #toDate = datetime.strptime(request.GET.get('to'),'%Y-%m-%d')
        fromd=request.GET.get('from','')
        tod=request.GET.get('to','')

        startdate=None
        enddate=None
       
        if '' != fromd:
            startdate = datetime.strptime(fromd[0:10], '%Y-%m-%d')
        if '' != tod:
            enddate = datetime.strptime(tod[0:10], '%Y-%m-%d') + timedelta(minutes=1439)

        queryset=search_queryset(fromDate=startdate, toDate=enddate,search='', is1=1, is0=0, ps1=0, ps2=0, ps3=0, relatedUser=-1, sessionProfile=0, fromDateP=None, toDateP=None, fromDateC=None, toDateC=None) 
        #i=Invoice.objects.filter(fac_cdate__gte=fromDate, fac_cdate__lte=toDate+timedelta(minutes=1439)).count()
        #print(i)
        #income=i['fac_total']i

        queryset= queryset.count()

        #if None == i:
        #    result=0
        #else:
        #    result=i
        
        if None == queryset:
            result =0
        else:
            result = queryset

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

    def get(self, request,*args,**kwargs):
        id = self.kwargs['id']
        queryset = InvoiceLog.objects.all().filter(log_invoice=int(id)).order_by('-log_datetime')
        
        serializer = InvoiceLogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        InvoiceLog.objects.all().filter(log_key=int(id)).delete()
        return Response('', status=status.HTTP_200_OK)

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

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        InvoiceReminders.objects.all().filter(rem_key=int(id)).delete()
        return Response(status=status.HTTP_200_OK)



class InvoicePaymentHistoryListingAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    #permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = InvoicePaymentHistorySerializer

    def get(self, request,*args,**kwargs):
        id = self.kwargs['id']
        queryset = InvoicePaymentHistory.objects.all().filter(his_invoice=id).order_by('-his_date')
        
        serializer = InvoicePaymentHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']

        payment= InvoicePaymentHistory.objects.all().filter(his_key=int(id))
        if payment:
            inv = payment[0].his_invoice

            InvoicePaymentHistory.objects.all().filter(his_key=int(id)).delete()

            qs=InvoicePaymentHistory.objects.filter(his_invoice=inv.fac_key).aggregate(s=Sum('his_amount'))
            payed=qs['s']

            if None == payed:
                result=0
            else:
                result=payed

            #paid=InvoicePaymentHistory.objects.get_sum_payments(id=inv)
            #print(result)
            i=Invoice.objects.get(pk=inv)
            i.fac_payments=result
            i.save()
 

        return Response(status=status.HTTP_200_OK)


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
    permission_classes = (IsAuthenticated,) #AllowAny, )

    def post(self,request):
        logdata=request.data
        user=request.user
        uid=user.id
        logdata['log_cuser']=id
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
        #iph=Invoice()
        qs=InvoicePaymentHistory.objects.filter(his_invoice=inv).aggregate(s=Sum('his_amount'))
        payed=qs['s']

        if None == payed:
            result=0
        else:
            result=payed

        #paid=InvoicePaymentHistory.objects.get_sum_payments(id=inv)
        #print(result)
        i=Invoice.objects.get(pk=inv)
        i.fac_payments=result
        i.save()

        return Response(serializer.data, status=status.HTTP_200_OK) #1_CREATED)

class InvoiceEdHistoryListingAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    #permission_classes = (AllowAny,)

    #queryset = User.objects.all().order_by('firstname')
    serializer_class = InvoiceEdHistorySerializer

    def get(self, request,*args,**kwargs):
        id = self.kwargs['id']
        queryset = InvoiceEdHistory.objects.all().filter(ed_invoice=id).order_by('-ed_newdate')
        
        serializer = InvoicePaymentHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']

        payment= InvoicePaymentHistory.objects.all().filter(his_key=int(id))
        if payment:
            inv = payment[0].his_invoice

            InvoicePaymentHistory.objects.all().filter(his_key=int(id)).delete()

            qs=InvoicePaymentHistory.objects.filter(his_invoice=inv.fac_key).aggregate(s=Sum('his_amount'))
            payed=qs['s']

            if None == payed:
                result=0
            else:
                result=payed

            #paid=InvoicePaymentHistory.objects.get_sum_payments(id=inv)
            #print(result)
            i=Invoice.objects.get(pk=inv)
            i.fac_payments=result
            i.save()
 

        return Response(status=status.HTTP_200_OK)

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': InvoiceSerializer(user).data
    }
