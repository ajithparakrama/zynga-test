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
from .forms import RecordForm,  MyUserCreationForm, userForm,UserChangeForm, RecordApproveForm
from .table import RecordTable, RecordTableAdmin





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
 
# @login_required(login_url='login')
# def home(request):    
#     records = record.objects.all()   
    
#     #records = record.objects.get(create_by = request.user)    fa
#     # record_count = records.count()
#     paginator = Paginator(records, 20)   
   
   
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {'page_obj':page_obj}
#     return render(request, 'base/home.html',context)

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