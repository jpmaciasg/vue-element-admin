from rest_framework import serializers
from .models import Invoice, InvoiceLog, InvoiceReminders, InvoicePaymentHistory,InvoiceEdHistory
from users.models import User
 
 
class InvoiceSerializer(serializers.ModelSerializer):
 
    #date_joined = serializers.ReadOnlyField()
    fac_key = serializers.IntegerField(read_only=True)
    fac_serie= serializers.CharField(read_only=True)
    fac_folio= serializers.IntegerField(read_only=True)
    fac_emisorrfc= serializers.CharField(read_only=True)
    fac_emisornombre= serializers.CharField(read_only=True)
    fac_receptorrfc= serializers.CharField(read_only=True)
    fac_receptornombre= serializers.CharField(read_only=True)
    fac_xml= serializers.CharField(read_only=True)
    fac_total= serializers.DecimalField (read_only=True, max_digits=16, decimal_places=6)
    #fac_observaciones= serializers.CharField(read_only=True)
    #fac_fechapago= serializers.DateField(read_only=True)
    fac_fecha= serializers.DateTimeField(read_only=True)
    fac_cdate= serializers.DateTimeField(read_only=True)
    fac_subtotal= serializers.DecimalField(read_only=True, max_digits=16, decimal_places=6)
    fac_iva= serializers.DecimalField(read_only=True, max_digits=16, decimal_places=6)
    #fac_payments= serializers.DecimalField(read_only=True, max_digits=16, decimal_places=6)
    #fac_isactive= serializers.BooleanField(read_only=True)
    #fac_contact= serializers.CharField(read_only=True)
    fac_lastreminder= serializers.IntegerField(read_only=True)
    #fac_pagada= serializers.IntegerField(read_only=True)
    #fac_complemento= serializers.CharField(read_only=True)
    #fac_idclient= serializers.IntegerField(read_only=True)
    fac_iduser= serializers.PrimaryKeyRelatedField(
            queryset= User.objects.all(),
            required= False,
            allow_null=True
            #write_only=False
    )

    first_name = serializers.CharField(source = 'fac_iduser.first_name', read_only=True)
    last_name = serializers.CharField(source = 'fac_iduser.last_name', read_only = True)
    username = serializers.CharField(source = 'fac_iduser.username', read_only = True)
 
    class Meta(object):
        model = Invoice
        fields = ('fac_key','fac_serie','fac_folio', 'fac_emisorrfc', 'fac_emisornombre',
                  'fac_receptorrfc', 'fac_receptornombre', 'fac_total','fac_xml',
                  'fac_observaciones', 'fac_fechapago', 'fac_fecha',
                  'fac_cdate', 'fac_subtotal', 'fac_iva', 'fac_payments', 
                  'fac_isactive', 'fac_contact', 'fac_lastreminder', 'fac_pagada',
                  'fac_complemento', 'fac_idclient','fac_iduser', 'first_name', 'last_name', 'username','fac_expectedpaymentday','fac_edupdatescount')

        datatables_always_serialize = ('fac_key','fac_iduser')

class InvoiceNoXmlSerializer(serializers.ModelSerializer):
 
    #date_joined = serializers.ReadOnlyField()
    fac_key = serializers.IntegerField(read_only=True)
    fac_debt = serializers.ReadOnlyField()
    fac_pagadatext=serializers.ReadOnlyField()
    fac_isactivetext=serializers.ReadOnlyField()
    fac_iduser= serializers.PrimaryKeyRelatedField(
            queryset= User.objects.all(),
            required= False,
            allow_null=True
            #write_only=False
    )

    first_name = serializers.CharField(source = 'fac_iduser.first_name', read_only=True)
    last_name = serializers.CharField(source = 'fac_iduser.last_name', read_only = True)
    username = serializers.CharField(source = 'fac_iduser.username', read_only = True)
 
    class Meta(object):
        model = Invoice
        fields = ('fac_key','fac_serie','fac_folio', 
                  'fac_receptorrfc', 'fac_receptornombre', 'fac_total',
                  'fac_observaciones', 'fac_fechapago', 'fac_fecha',
                  'fac_cdate', 'fac_subtotal', 'fac_iva', 'fac_payments', 
                  'fac_isactive', 'fac_contact', 'fac_lastreminder', 'fac_pagada', 'fac_debt','fac_pagadatext',
                  'fac_complemento', 'fac_idclient','fac_iduser', 'first_name', 'last_name', 'username','fac_expectedpaymentday','fac_isactivetext','fac_edupdatescount')

        datatables_always_serialize = ('fac_key','fac_iduser','username')


class InvoiceLogSerializer(serializers.ModelSerializer):
 
    #date_joined = serializers.ReadOnlyField()
    log_key = serializers.IntegerField(read_only=True)
    #log_invoice = serializers.IntegerField(read_only=True)
    log_invoice=serializers.PrimaryKeyRelatedField(
            queryset=Invoice.objects.all(),
            required=True,
            write_only=False,
            allow_null=True
    )

    log_cuser = serializers.PrimaryKeyRelatedField(
            queryset = User.objects.all(),
            required= False,
            write_only=False
    )
    first_name = serializers.CharField(source = 'log_cuser.first_name', read_only=True)
    last_name = serializers.CharField(source = 'log_cuser.last_name', read_only = True)
    username = serializers.CharField(source = 'log_cuser.username', read_only = True)

    class Meta(object):
        model = InvoiceLog
        fields = ('log_key','log_text','log_datetime', 'log_invoice', 'log_invoice', 'log_cuser', 'first_name','last_name','username',)

        datatables_always_serialize = ('log_key','log_cuser',)

class InvoiceReminderSerializer(serializers.ModelSerializer):
 
    #date_joined = serializers.ReadOnlyField()
    rem_key = serializers.IntegerField(read_only=True)
    #rem_invoice = serializers.IntegerField(read_only=True)
    rem_invoice=serializers.PrimaryKeyRelatedField(
            queryset=Invoice.objects.all(),
            required=True,
            write_only=False
    )
    rem_cuser = serializers.PrimaryKeyRelatedField(
            queryset= User.objects.all(),
            required= False,
            write_only=False,
            allow_null=True
    )

    first_name = serializers.CharField(source = 'rem_cuser.first_name', read_only=True)
    last_name = serializers.CharField(source = 'rem_cuser.last_name', read_only = True)
    username = serializers.CharField(source = 'rem_cuser.username', read_only = True)


    class Meta(object):
        model = Invoice
        fields = ('fac_key','fac_serie','fac_folio', 'fac_emisorrfc', 'fac_emisornombre',
                  'fac_receptorrfc', 'fac_receptornombre', 'fac_total','fac_xml',
                  'fac_observaciones', 'fac_fechapago', 'fac_fecha',
                  'fac_cdate', 'fac_subtotal', 'fac_iva', 'fac_payments',
                  'fac_isactive', 'fac_contact', 'fac_lastreminder', 'fac_pagada',
                  'fac_complemento', 'fac_idclient','fac_iduser', 'first_name','last_name','username',)

        datatables_always_serialize = ('fac_key')


class InvoicePaymentHistorySerializer(serializers.ModelSerializer):
 
    #date_joined = serializers.ReadOnlyField()
    his_key = serializers.IntegerField(read_only=True)
    #his_invoice = serializers.IntegerField(read_only=True)
    his_invoice = serializers.PrimaryKeyRelatedField(
            queryset=Invoice.objects.all(),
            required=True,
            write_only=False
    )
 
    class Meta(object):
        model = InvoicePaymentHistory
        fields = ('his_key','his_invoice','his_date', 'his_amount', )

        datatables_always_serialize = ('his_key',)

class InvoiceEdHistorySerializer(serializers.ModelSerializer):
    
    ed_key = serializers.IntegerField(read_only=True)
    ed_invoice = serializers.PrimaryKeyRelatedField(
            queryset=Invoice.objects.all(),
            required=True,
            write_only=False
    )

    ed_user = serializers.PrimaryKeyRelatedField(
            queryset = User.objects.all(),
            required= True,
            write_only=False
    )

    username = serializers.CharField(source = 'ed_user.username', read_only = True)



    class Meta(object):
        model = InvoiceEdHistory
        fields = ('ed_key','ed_invoice','ed_newdate', 'ed_olddate', 'ed_user','username',)

        datatables_always_serialize = ('ed_key',)
'''
class PromotorPieSerializer(serializers.BaseSerializer):
    promotor = serializers.CharField(read_only=True)
 
    class Meta(object):
        fields = ('income', 'promotor')
        datatables_always_serialize = ('promotor',)
'''
