from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import record, User




class RecordForm(ModelForm):
    class Meta:
        model = record
        fields = '__all__'
        exclude = ['create_by','approve_time','approve_status']
      #  fields = ('record_id', 'company_code', 'functional_area_id')
      #  widgets = {
      #      'record_id': CharField(attrs={'class': 'form-control', 'placeholder': 'Record Id'}),
     #   }
class RecordApproveForm(ModelForm):
    class Meta:
        model = record
        fields = '__all__'
        exclude = ['create_by','approve_time']
     
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
       # fields = '__all__'
        fields = ['username', 'first_name','last_name','email','password1' ,'password2']
       
    
        
class userForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        
        
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        
        fields = ['avatar', 'first_name','last_name','email']

class UserChangeFormAdmin(UserChangeForm):
    class Meta:
        model = User        
        fields = ['first_name','last_name','email','user_type']