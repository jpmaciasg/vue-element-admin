# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractUser
)
from django.db import transaction

class Role(models.Model):
    role_key = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=30, null = False, unique=True )
    role_label = models.CharField(max_length=300, null = True )
    role_description =models.TextField(null=True, blank=True)
    role_weight = models.IntegerField(null = False)
    
    def __str__(self):
        return self.role_name
        
    class Meta:
        managed = False
        db_table = 'cbr_roles'
        
class User(AbstractUser):
    #rolename = models.CharField(max_length=30, null = False, default='promotor')
    #rolename= models.ForeignKey(Role, to_field= 'role_name', db_column = 'rolename', on_delete = '') 
    rolename=  models.CharField(max_length=30, null = True, blank=True)
    role_key = models.ForeignKey(Role, to_field='role_key', db_column = 'role_key', on_delete = '')
    email = models.CharField(blank=True, null=True, max_length=254)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role_key', 'email']
    #pass
 
    def __str__(self):
        return self.username
        
    class Meta:
        db_table = 'crm_user'
        ordering = ['username','first_name','last_name','role_key', 'role_key__role_label']


