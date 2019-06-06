from django.db import models
from users.models import User

# Create your models here.

class Contact (models.Model):
    id = models.AutoField(primary_key=True)
    contact_firstname = models.CharField(max_length=100, null = True) #character varying(30) NOT NULL,
    contact_lastname = models.CharField(max_length=100, null = True) # character varying(50) NOT NULL,
    contact_type = models.CharField(max_length=30, null = False) 
    contact_fullname = models.CharField(max_length=100, null = True) # character varying(100),
    contact_byname = models.CharField(max_length=100, null = False) #boolean NOT NULL DEFAULT true,
    contact_cdate = models.DateField(auto_now_add = True )
    contact_mdate = models.DateField( auto_now=True )
    contact_address = models.TextField(null=True, blank=True) # Will be moved to profile
    contact_email = models.TextField(null=True, blank=True) # Will be moved to profile
    contact_taxid = models.TextField(null=True, blank=True) # Will be moved to profile
    contact_phone = models.TextField(null=True, blank=True) # Will be moved to profile
    contact_comment = models.TextField(null=True, blank=True)
    #Profile = JSONField()

    class Meta:
        db_table = 'contact'
        ordering = ['contact_firstname','contact_lastname','contact_fullname','contact_taxid','contact_email', 'contact_type']

class ContactUser (models.Model):
    id = models.AutoField(primary_key=True)
    cu_contact_id = models.ForeignKey(Contact, to_field= 'id', db_column = 'cu_contact_id', on_delete = '') 
    cu_id = models.ForeignKey(User, to_field= 'id', db_column = 'cu_id', on_delete = '') 
    
    class Meta:
        db_table = 'contact_user'

class ContactStaging (models.Model):
    rawname = models.CharField(max_length=200, null = True)
    name = models.CharField(max_length=200, null = True)
    db = models.CharField(max_length=20, null = True)
    user= models.CharField(max_length=30, null = True)
    
    class Meta:
        db_table = 'contact_staging'

