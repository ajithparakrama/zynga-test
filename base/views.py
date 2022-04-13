from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout 
from .models import record, User
from .forms import RecordForm,  MyUserCreationForm, userForm,UserChangeForm
from .table import RecordTable 



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
    
    return render(request, 'base/profile.html',{'form':form})
 
@login_required(login_url='login')
def home(request):    
    records = record.objects.all()   
    
    #records = record.objects.get(create_by = request.user)    
    # record_count = records.count()
    paginator = Paginator(records, 20)   
   
   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    return render(request, 'base/home.html',context)

@login_required(login_url='login')
def allview(request):
    table = RecordTable(record.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=20)
    return render(request, "base/records.html", {
        "table": table
    })
    
"""
def allview(SingleTableView):
    model = record
    table_class = RecordTable
    template_name = 'base/records.html'
"""
    
    

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

