from rest_framework import serializers
from .models import Contact , ContactUser
from users.serializers import UserSerializer
from users.models import User
 
 
class ContactSerializer(serializers.ModelSerializer):
 
    #date_joined = serializers.ReadOnlyField()
    id = serializers.IntegerField(read_only=True)
    contact_type = serializers.CharField(read_only=True)
    
 
    class Meta(object):
        model = Contact
        fields = ('id',
            'contact_firstname' ,
            'contact_lastname' ,
            'contact_type' ,
            'contact_fullname',
            'contact_byname' ,
            'contact_cdate' ,
            'contact_mdate',
            'contact_address',
            'contact_email',
            'contact_taxid',
            'contact_phone',
            'contact_comment'
        )

        datatables_always_serialize = ('id',)

        depth = 3

class ContactUserSerializer(serializers.ModelSerializer):
 
    #date_joined = serializers.ReadOnlyField()
    id = serializers.IntegerField(read_only=True)
 
    class Meta(object):
        model = Contact
        fields = ('id','cu_contact_id' ,
            'cu_id' 
        )

        datatables_always_serialize = ('id',)

class ContactListSerializer(serializers.ModelSerializer):
    #contact = ContactSerializer(many=True, required=True)
    #contactuser = ContactUserSerializer(many=True, required=False)  # A nested list of 'edit' items.
    #user = UserSerializer(required=False)
    contactuser__cu_id__username = serializers.ReadOnlyField()

    class Meta(object):
        model = Contact
        fields = (
            'id',
            'contact_firstname' ,
            'contact_lastname' ,
            'contact_type' ,
            'contact_fullname',
            'contact_byname' ,
            'contact_cdate' ,
            'contact_mdate',
            'contact_address',
            'contact_email',
            'contact_taxid',
            'contact_phone','contactuser__cu_id__username'
        )

        datatables_always_serialize = ('id','contact_type')

        depth = 3
    
