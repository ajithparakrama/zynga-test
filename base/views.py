import datetime
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout 
from .models import record, User
from .forms import RecordForm,  MyUserCreationForm, userForm,UserChangeForm, RecordApproveForm,UserChangeFormAdmin
from .table import RecordTable, RecordTableAdmin,AdminUsers
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes





def loginPage(request):
        page = 'login'
        if request.user.is_authenticated:
            return redirect('home')
        
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request,'User Does not exist')     
                
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or Password does not exits')
            
        context = {'page' : page}
        return render(request, 'base/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request): 
     form = MyUserCreationForm()
     
     if request.method =='POST':
         form = MyUserCreationForm(request.POST,request.FILES)
         if form.is_valid():
             user = form.save(commit=False)
             user.username = user.username.lower()
             user.save()
             login(request, user)
             return redirect('home')
         else: 
            messages.error(request, 'An error occured during registration')
   #  context = {'page' : page}
     return render(request, 'base/register.html',{'form' : form})

def fogot(request):
    
    return render(request,'base/fogot.html')

def about(request):
    return render(request,'base/about.html')

def profile(request):
    form = UserChangeForm(instance=request.user)
    if request.method == 'POST':
        form = UserChangeForm(request.POST,request.FILES,instance=request.user) 
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request, 'base/profile.html',{'form':form})

def changepass(request):
    form = userForm(request.user)
    if request.method == 'POST':
        form.userForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request,'base/change-password.html',{'form':form})
 
@login_required(login_url='login')
def allview(request):
    
    if request.user.user_type==True:
        #
        try:
            table = RecordTableAdmin(record.objects.all())
            table.paginate(page=request.GET.get("page", 1), per_page=20)
        except:
            table = None
            
        return render(request, "base/allrecords.html", {
            "table": table
        })
    else:
        try:
            table = RecordTable(record.objects.filter(create_by=request.user))
            table.paginate(page=request.GET.get("page", 1), per_page=20)
        except:
            table = None
            
        return render(request, "base/records.html", {
            "table": table
        }) 


@login_required(login_url='login')
def newrecord(request):
    form = RecordForm()
    
    if request.method=='POST':
        form = RecordForm(request.POST)
        if form.is_valid():            
            record = form.save(commit=False)
            record.create_by = request.user
            record.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/createRecord.html',context)

@login_required(login_url='login')
def editrecord(request, pk):
    er = record.objects.get(id=pk)
    form = RecordForm(instance=er)
    
    #if this is not the user that create the record
    if er.create_by !=  request.user :
        return HttpResponse('You are not allowed here')
    
    if request.method =='POST':
        form = RecordForm(request.POST, instance=er)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    context = {'form':form}
    return render(request, 'base/editRecord.html',context)

@login_required(login_url='login')
def approverecord(request, pk):
    er = record.objects.get(id=pk)
    form = RecordApproveForm(instance=er)

    if request.method =='POST':
        form = RecordApproveForm(request.POST, instance=er)
        if form.is_valid():
            form = form.save(commit=False)
            form.approve_time = datetime.datetime.now()
            form.save()
            return redirect('home')
            
    context = {'form':form}
    return render(request, 'base/approveRecord.html',context)

def export_record(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="record.csv"'

    writer = csv.writer(response)
    writer.writerow(['Record ID', 'Company Code', 'Functional Area', 'Cost Center','Plan Type','Year','Investment Priority','Assets Type','Capex Type','Preview Number','Asset to be Replace','Expected Inverstment Value','Expected Servince Category','Expected Savings Value','Project Start Date','Project End Date','Status','Confirmation','Approve Status'])
    users = record.objects.all()
    for user in users:
        writer.writerow([user.record_id,user.company_code, user.functional_area,user.cost_center,user.plan_type,user.year,user.investment_priority,user.assets_type, user.capex_type,user.preview_number,user.asset_to_be_replace,user.expected_inverstment_value,user.expected_servince_category,user.expected_savings_value,user.project_start_date,user.project_end_date,user.status,user.confirmation,user.approve_status])

    return response

def export_record_user(request):    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="record.csv"'

    writer = csv.writer(response)
    writer.writerow(['Record ID', 'Company Code', 'Functional Area', 'Cost Center','Plan Type','Year','Investment Priority','Assets Type','Capex Type','Preview Number','Asset to be Replace','Expected Inverstment Value','Expected Servince Category','Expected Savings Value','Project Start Date','Project End Date','Status','Confirmation','Approve Status'])
    users = record.objects.filter(create_by=request.user)
    for user in users:
        writer.writerow([user.record_id,user.company_code, user.functional_area,user.cost_center,user.plan_type,user.year,user.investment_priority,user.assets_type, user.capex_type,user.preview_number,user.asset_to_be_replace,user.expected_inverstment_value,user.expected_servince_category,user.expected_savings_value,user.project_start_date,user.project_end_date,user.status,user.confirmation,user.approve_status])

    return response

def user_accounts(request):
 
   # table = User.objects.all()
    table = User.objects.all()
  #  print(vars(table))
  #  table.paginate(page=request.GET.get("page", 1), per_page=20)
    return render(request, "base/users.html", { "table": table })  

def edit_user(request, pk):
    er = User.objects.get(id=pk)
    form = UserChangeFormAdmin(instance=er) 
    
    if request.method == 'POST':
        form.UserChangeFormAdmin(request.POST, instance=er)
        if form.is_valid:
            form.save()
            return redirect('user-accounts')
    return render(request,'base/admin-change-user.html',{'form':form}) 


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@localhost.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def password_reset_request(request):
    if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "main/password/password_reset_email.txt"
                        c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                        except BadHeaderError:

                            return HttpResponse('Invalid header found.')
                           
                        messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                        return redirect ("main:homepage")
    
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})
