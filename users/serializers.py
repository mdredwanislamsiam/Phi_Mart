from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer




class UserCreateSerializer(BaseUserCreateSerializer): 
    class Meta(BaseUserCreateSerializer.Meta): 
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'password']
        



class UserSerializer(BaseUserSerializer): 
    
    class Meta(BaseUserSerializer.Meta): 
        fields = ['id', 'first_name', 'last_name', 'address', 'phone_number', 'email', "is_staff"]
        ref_name = 'CustomUser'
        read_only_fields =["is_staff"]