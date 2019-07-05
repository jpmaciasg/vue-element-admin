from django.core.management.base import BaseCommand,CommandError
from invoices.models import Invoice as Invoice, InvoiceFileLog as InvoiceFileLog
from invoices.serializers import InvoiceFileLogSerializer
import io
from datetime import datetime

class Command(BaseCommand):
    help = 'Adds invoice from filesystem'

    #def add_arguments(self, parser):
    #    parser.add_argument('file', nargs='+', type = str)

    def handle(self, *args, **options):

        fl=InvoiceFileLog.objects.filter(ifl_status='PENDING')
        
        for e in fl:
            data={}
            i=InvoiceFileLog.objects.get(pk=e.ifl_key)
            i.ifl_status='PROCESSING'
            i.save()
            
            f=e.ifl_filepath
            x=Invoice()
            xml=open(f,"rb")
            x.upload(xml)
            
            i.ifl_status='DONE'
            i.ifl_pdate=datetime.now()
            i.save()

            #i2=InvoiceFileLog.objects.get(pk=e.ifl_key)
            #serializer2=InvoiceFileLogSerializer(i2,data=data)
            #if serializer2.is_valid():
            #    serializer2.save(raise_exception=True)

            



        
