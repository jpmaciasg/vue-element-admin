from django.core.management.base import BaseCommand,CommandError
from invoices.models import Invoice as Invoice, InvoiceFileLog as InvoiceFileLog
from invoices.serializers import InvoiceFileLogSerializer
import io
from datetime import datetime

class Command(BaseCommand):
    help = 'Adds invoice from filesystem'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type = str)

    def handle(self, *args, **options):

        fl=InvoiceFileLog.objects.filter(Q(ifl_status='PENDING'))
        
        for e in fl:
            data={}
            i=InvoiceFileLog.objects.get(pk=e.ifl_key)
            data['ifl_status']='PROCESSING'
            serializer=InvoiceFileLogSerializer(i,data=data)
            if serializer.is_valid():
                serializer.save(raise_exception=True)
            
            f=e.ifl_filepath
            x=Invoice()
            xml=open(f,"rb")
            x.upload(xml)
            data['ifl_status']='DONE'
            data['ifl_pdate']=datetime.datetime.now()

            i=InvoiceFileLog.objects.get(pk=e.ifl_key)
            serializer=InvoiceFileLogSerializer(i,data=data)
            if serializer.is_valid():
                serializer.save(raise_exception=True)

            



        
        #f=options['file'][0]
        #print(f)
        #for f in options['file']:
        #try:
                #code to generate new  invoice
                # poll = Poll.objects.get(pk=poll_id)
                #x=new Invoice()
            #self.stdout.write(self.style.SUCESS('Add file "%s"' % f))
            #print("add ",f)
        

        #xml=open(f,"rb")
        #print(xml)
        x.create_log(f)
        #print("Added", f)
        #except : #Invoice.DoesNotExists:
        #    raise CommandError('Error adding invoice from file "%s"' % f)

            #code to complete

        #self.stdout.write(self.style.SUCCESS('Added invoice from file "%s"' % f))

