from django.db import models
from django.db import connection
import datetime
from users.models import User
from contacts.models import ContactStaging, Contact,ContactUser
import xml.etree.ElementTree as ET
import os

# Create your models here.

class Invoice (models.Model):
    fac_key = models.AutoField(primary_key=True)
    fac_serie = models.CharField(max_length=10, null = False)
    fac_folio = models.IntegerField(null = False)
    fac_emisorrfc = models.CharField(max_length=30, null = False)
    fac_emisornombre = models.TextField(null=False, blank=False)
    fac_receptorrfc = models.CharField(max_length=30, null = False)
    fac_receptornombre = models.TextField(null=False, blank=False)
    fac_total = models.DecimalField(decimal_places=6,max_digits=16, default=0, null = False)
    fac_observaciones = models.TextField(null=True, blank=True)
    fac_xml =models.TextField(null=False, blank=False)
    fac_fechapago =models.DateField(null=True, blank=True)
    fac_fecha = models.DateTimeField(null=False, blank=False)
    fac_cdate = models.DateTimeField(null=True, default=datetime.date.today)
    fac_subtotal =models.DecimalField(decimal_places=6,max_digits=16, default=0, null = False)
    fac_iva =models.DecimalField(decimal_places=6,max_digits=16, default=0, null = False)
    fac_payments =models.DecimalField(decimal_places=6,max_digits=16, default=0, null = False)
    fac_isactive =models.BooleanField(null=False, default= True)
    fac_contact = models.TextField(null=True, blank=True)
    fac_lastreminder = models.IntegerField(null = False, default=0)
    fac_pagada = models.IntegerField(null = False, default=2)
    fac_complemento = models.TextField(null = True, blank=True)
    #fac_idclient = models.IntegerField(null = True, default=0)
    fac_idclient=models.ForeignKey(Contact, to_field='id', db_column = 'fac_idclient', on_delete = '', null=True, blank=True)
    #fac_iduser= models.IntegerField(null = True, default=0)
    fac_iduser=models.ForeignKey(User, to_field='id', db_column = 'fac_iduser', on_delete = '', null=True, blank=True)
    fac_expectedpaymentday = models.DateField(null=True, blank=True)
    fac_edupdatescount =models.IntegerField(null=True, blank=True, default =0)

    @property
    def fac_debt(self):
        return self.fac_total - self.fac_payments

    @property
    def fac_pagadatext(self):
        ret=''
        if self.fac_pagada==1:
            ret='PAGADA'
        elif self.fac_pagada==2:
            ret='NO PAGADA'
        elif self.fac_pagada==3:
            ret='CONFIRMAR'

        return ret

    @property
    def fac_isactivetext(self):
        ret=''
        if self.fac_isactive==True:
            ret ='ACTIVA'
        elif self.fac_isactive==False:
            ret ='CANCELADA'

        return ret

    @property
    def fac_daysopen(self):
        d=0
        if self.fac_pagada == None:
            d=datetime.now().date() - self.fac_fecha
        else:
            d=self.fac_fechapago - self.fac_fecha

        return d.days



    class Meta:
        managed = False
        db_table = 'cbr_facturas'
        unique_together = ('fac_serie', 'fac_folio','fac_emisorrfc',)
        indexes = [
            models.Index(fields=['fac_idclient','fac_iduser']),
        ]

    def missing_invoices(self):
        r = connection.cursor()

        query = """
        select w.fac_serie, w.f as fac_folio from  (
            select fac_serie, generate_series(l,m) as f from (
                select fac_serie, max(fac_folio) as m, min(fac_folio) as l from cbr_facturas where extract(year from fac_fecha) = extract(year from now()) group by fac_serie
            ) z 
        ) w
        left join cbr_facturas f on f.fac_serie=w.fac_serie and f.fac_folio=w.f 
        where f.fac_folio is null
        order by 1 desc, 2 desc
        """

        row = None
        with connection.cursor() as cursor:
            cursor.execute(query)

            row = [{"fac_serie" : item[0], "fac_folio": item[1]} for item in cursor.fetchall()]

        return row

    def upload(self, filepath):
        #print('en model upload' + filepath.path)

        nsmap = {}
        #f2=os.path.realpath(filepath.name)
        #print(f2)

        #with open(f2) as f2f:
        #    xmlcontent = f2f.read()
        #print("antes")
        xmlstr=filepath.read()
        u=xmlstr.decode("utf-8-sig")
        xmlstr=u.encode("utf-8")
        xmlstr=xmlstr.decode("utf-8")
        #print(xmlstr)
        root=ET.fromstring(xmlstr)
        nsmap['cfdi']='http://www.sat.gob.mx/cfd/3'
        #tree=ET.parse(filepath)
        #root=tree.getroot()
        version=root.get('version')
        if None==version:
            version=root.get('Version')
        
        if version=="3.2":
            atFolio="folio"
            atSerie="serie"
            atFecha="fecha"
            atSubtotal="subTotal"
            atTotal="total"
            atEmisorRfc="rfc"
            atEmisorNombre="nombre"
            atReceptorRfc="rfc"
            atReceptorNombre="nombre"
        
        if version=="3.3":
            atFolio="Folio"
            atSerie="Serie"
            atFecha="Fecha"
            atSubtotal="SubTotal"
            atTotal="Total"
            atEmisorRfc="Rfc"
            atEmisorNombre="Nombre"
            atReceptorRfc="Rfc"
            atReceptorNombre="Nombre"

        inv={}
        inv['fac_xml'] = xmlstr #xmlcontent

        inv['fac_folio']=root.get(atFolio)
        s=root.get(atSerie)
        if None==s:
            s=' '
        inv['fac_serie']=s
        inv['fac_fecha']=root.get(atFecha)
        inv['fac_total']=root.get(atTotal)
        inv['fac_subtotal']=root.get(atSubtotal)
        

        for child in root:
            tag=self.gettag('cfdi',child.tag, nsmap)
            #print(tag)
            if tag =='Emisor':
                inv['fac_emisorrfc']=child.get(atEmisorRfc)
                inv['fac_emisornombre']=child.get(atEmisorNombre)
            if tag =='Receptor':
                inv['fac_receptorrfc']=child.get(atReceptorRfc)
                inv['fac_receptornombre']=child.get(atReceptorNombre)
            if tag == 'Impuestos':
                for child2 in child:
                    for child3 in child2:
                        impuesto= child3.get('Impuesto')
                        if impuesto == '002':
                            inv['fac_iva']=child3.get('Importe')


        inv['fac_key']=None
        inv['fac_idclient']=None
        inv['fac_iduser']=None

        #print(inv)
        
        if Contact.objects.filter(contact_taxid=inv['fac_receptorrfc']).exists():
            client=Contact.objects.get(contact_taxid=inv['fac_receptorrfc'])
            inv['fac_idclient']=client
            if ContactUser.objects.filter(cu_contact_id=client).exists():
                cu=ContactUser.objects.get(cu_contact_id=client)
                inv['fac_iduser']=cu.cu_id
        
        else:
            cdata = {}
            cdata['contact_fullname']=inv['fac_receptornombre']
            cdata['contact_taxid']=inv['fac_receptorrfc']
            cdata['contact_type']='company'
            c=Contact(**cdata)
            c.save()

            inv['fac_idclient']=c.id

    

        i=Invoice(**inv)
        i.save()



    def income_from_dates(self, fromDate, toDate):
        result=0
        income=self.objects.filter(fac_fechapago__range=[fromDate, toDate]).aggregate(fac_total=Sum('fac_total'))
        if None == income:
            result=0
        else:
            result = income['fac_total']

        return result

    def promotor_pie_data(self, fromDate, toDate):
        r = connection.cursor()

        query = """
        select sum(fac_total) as income, case when u.first_name is null then 'None' else u.first_name || ' ' || u.last_name  end as promotor
        from cbr_facturas f left join contact_user c on f.fac_idclient=c.cu_contact_id 
        left join crm_user u on c.cu_id=u.id
        """
        query = query + ' where fac_pagada=1 and fac_fechapago between \'' + fromDate + '\'  and \'' + toDate + '\'' 
        query = query + " group by u.first_name, u.last_name "
        #print(query)

        rows = None
        with connection.cursor() as cursor:
            cursor.execute(query)

            rows=[item[0] for item in cursor.fetchall()]

        return rows
    
    def fixtag(self,ns, tag, nsmap):
        if (ns == ''):
            return tag
        else:
            return '{' + nsmap[ns] + '}' + tag

    def gettag(self,ns,fulltag,nsmap):
        if (ns == ''):
            return fulltag
        else:
            return fulltag.replace('{' + nsmap[ns] + '}', '')

class InvoiceLog(models.Model):
    log_key = models.AutoField(primary_key=True)
    #log_invoice = models.IntegerField(null = False)
    log_text =models.TextField(null=False, blank=False)
    log_datetime = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    log_invoice = models.ForeignKey(Invoice, to_field= 'fac_key', db_column = 'log_invoice', on_delete = '')
    log_cuser = models.ForeignKey(User, to_field = 'id', db_column = 'log_cuser', on_delete = '', blank=True, null=True)

    class Meta:
       managed = False
       db_table = 'cbr_bitacoras'
       ordering = ['log_datetime', 'log_cuser', 'log_cuser__first_name', 'log_cuser__last_name']


class InvoiceReminders(models.Model):
    rem_key = models.AutoField(primary_key=True)
    rem_invoice = models.ForeignKey(Invoice, to_field= 'fac_key', db_column = 'rem_invoice', on_delete = '') 
    rem_text =models.TextField(null=False, blank=False)
    rem_datetime = models.DateTimeField(null=False, blank=False)
    rem_isactive  =models.BooleanField(null=False, default= True)
    rem_cuser = models.ForeignKey(User, to_field='id', db_column = 'rem_cuser', on_delete = '', blank = True, null = True)

    class Meta:
       managed = False
       db_table = 'cbr_reminders'



class InvoicePaymentHistory(models.Model):

    his_key = models.AutoField(primary_key=True)
    his_invoice = models.ForeignKey(Invoice, to_field= 'fac_key', db_column = 'his_invoice', on_delete = '') 
    his_date  =models.DateField(null=False, blank=False)
    his_amount = models.DecimalField(decimal_places=6,max_digits=16, default=0, null = False)

    class Meta:
       managed = False
       db_table = 'cbr_historialpagos'

class InvoiceEdHistory(models.Model):

    ed_key = models.AutoField(primary_key=True)
    ed_invoice = models.ForeignKey(Invoice, to_field= 'fac_key', db_column = 'his_invoice', on_delete = '') 
    ed_newdate  =models.DateTimeField(null=False, blank=False)
    ed_olddate  =models.DateTimeField(null=False, blank=False)
    ed_user = models.ForeignKey(User, to_field='id', db_column = 'ed_user', on_delete = '', blank = True, null = True)

    class Meta:
       managed = True
       db_table = 'cbr_edhistory'

