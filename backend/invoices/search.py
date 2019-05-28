from django.shortcuts import render
from django.contrib.auth import get_user_model
import warnings
from django.conf import settings
from .models import Invoice, InvoiceLog, InvoiceReminders, InvoicePaymentHistory
from django.db.models import Avg, Count, Min, Sum, Q
from datetime import datetime, timedelta
import logging
from users.models import User, Role

def search_queryset(fromDate, toDate, search, is1, is0, ps1, ps2, ps3, relatedUser, sessionProfile, fromDateP, toDateP):

        queryset = Invoice.objects.all()

        # Specific search for Promotors
        if sessionProfile == 3 :
            queryset = queryset.filter(fac_isactive= True, fac_pagada=2, fac_iduser=relatedUser)
        else:
            if relatedUser != 0 :
                queryset = queryset.filter(fac_iduser = relatedUser)

            if ps1 > 0 or ps2 > 0 or ps3 > 0:
                q_pay=Q()

                if ps1 > 0:
                    q_pay |= Q(fac_pagada = 1)
                if ps2 > 0: 
                    q_pay |= Q(fac_pagada = 2)

                if ps3 > 0:
                    q_pay |= Q(fac_pagada = 3)

                queryset=queryset.filter( q_pay )

            if is1 > 0 or is0 > 0:
                q_act = Q()

                if is1 > 0:
                    q_act |= Q(fac_isactive = True)

                if is0 > 0:
                    q_act |= Q(fac_isactive = False)

                queryset = queryset.filter( q_act )

            if fromDate != None or toDate != None :
                q_date= Q()

                if fromDate != None:
                    q_date &= Q(fac_fecha__gte=fromDate)

                if toDate != None:
                    q_date &= Q(fac_fecha__lte=toDate)

                queryset = queryset.filter(q_date)

            if fromDateP !=None or toDateP != None:
                q_datep = Q()

                if fromDateP != None:
                    q_datep &= Q(fac_fechapago__gte=fromDateP)

                if toDateP != None: 
                    q_datep &= Q(fac_fechapago__lte =toDateP)

                queryset = queryset.filter(q_datep)

            if search != '':
                q_search = Q()

                q_search |= Q(fac_folio__icontains = search)
                q_search |= Q(fac_receptornombre__icontains = search)
                q_search |= Q(fac_receptorrfc__icontains = search)

                queryset = queryset.filter( q_search )



        return queryset
    


