from django.core.management.base import BaseCommand,CommandError
from invoices.models import Invoice as Invoice
import io

class Command(BaseCommand):
    help = 'Adds invoice from filesystem'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type = str)

    def handle(self, *args, **options):
        f=options['file'][0]
        print(f)
        #for f in options['file']:
        #try:
                #code to generate new  invoice
                # poll = Poll.objects.get(pk=poll_id)
                #x=new Invoice()
            #self.stdout.write(self.style.SUCESS('Add file "%s"' % f))
            #print("add ",f)
        x=Invoice()
        xml=open(f,"rb")
        print(xml)
        x.upload(xml)
        #print("Added", f)
        #except : #Invoice.DoesNotExists:
        #    raise CommandError('Error adding invoice from file "%s"' % f)

            #code to complete

        #self.stdout.write(self.style.SUCCESS('Added invoice from file "%s"' % f))

