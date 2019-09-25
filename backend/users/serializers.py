from rest_framework import serializers
from .models import User, Role
from drf_writable_nested import WritableNestedModelSerializer
 

class RoleSerializer(serializers.ModelSerializer):
 
    role_key = serializers.IntegerField(read_only=True)
 
    class Meta(object):
        model = Role
        fields = ('role_key', 'role_name','role_label', 'role_description', 'role_weight')

        datatables_always_serialize = ('role_key',)


class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
    id = serializers.IntegerField(read_only=True)

    role_key=serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=True,
        #source='role_key',
        write_only=False
    )
    role_label = serializers.CharField(source='role_key.role_label', read_only=True)
    role_name = serializers.CharField(source='role_key.role_name', read_only=True)

    #rolename = User.ForeignKey(Role, related_name='role_name')
    #rolename = serializers.CharField(read_only=True,source='Role.role_name')
   
    #rolename = RoleSerializer(many=False, read_only=True)
    #rolename=RoleSerializer()
    #role__role_label = serializers.ReadOnlyField()
    #rolename = serializers.SlugRelatedField(queryset=Role.objects.all(),slug_field='role_name')
    #rolelabel = serializers.SlugRelatedField(slug_field='role_label', read_only=True)
 
    class Meta(object):
        model = User
        fields = ('id', 'username','email', 'first_name', 'last_name',
                  'date_joined', 'password', 'role_key', 'role_label',
                  'avatar','role_name','is_active')
        extra_kwargs = {'password': {'write_only': True}}

        datatables_always_serialize = ('id',)
        depth = 2

    #def create(self, validated_data):
    #    print(validated_data)
    #    role=Role.objects.get(role_name=self.initial_data['rolename'])
    #    validated_data.rolename=role
    #    return User.objects.create(**validated_data)

    #def update(self, instance, validated_data):
    #    instance.username = validated_data.get('username', instance.username)
    #    instance.email = validated_data.get('email', instance.email)
    #    instance.first_name = validated_data.get('first_name', instance.first_name)

    #    instance.last_name = validated_data.get('last_name', instance.last_name)
    #    instance.password = validated_data.get('password', instance.password)
    #    instance.rolename = validated_data.get('rolename', instance.rolename)
    #    instance.save()

    #    return instance

