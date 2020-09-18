from django.http import HttpResponse
from django.shortcuts import render, redirect
from article_app.models import Users,Login,Article
from datetime import datetime
from .forms import ArticleForm
# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'registerForm.html')

def registeruser(request):

    name = request.POST.get('name')
    birthday = request.POST.get('birthday')
    gender = request.POST.get('gender')
    mobile = request.POST.get('mobile')
    username = request.POST.get('username')
    password = request.POST.get('password')

    d = datetime.strptime(birthday,'%d/%m/%Y') # converted in datetime format ...
    dob = datetime.strftime(d,'%Y-%m-%d') # converted from datetime into specific format ...
    request.session['name'] = name

    login_data = Login(user_name=username, password=password)
    login_data.save()
    l_id = Login.objects.get(user_name=username,password=password)
    # print(l_id.id)
    register_user = Users(name=name,username=username,DOB =dob,gender=gender,mobile=mobile,password=password,login_id=l_id)
    register_user.save()


    return redirect(user_dashboard)

def user_dashboard(request):
    if request.session['login_id'] :
        l_id = int(request.session.get('login_id'))
        Name = Users.objects.get(login_id=l_id).name
        request.session['name'] = Name

    return render(request,'user_Dashboard.html')

def logout(request):
    request.session.clear()
    return redirect(index)

def login(request):
    return render(request,'login.html')

def getlogin(request):
    username= request.POST.get('username')
    password = request.POST.get('password')
    # print(username ,"       ",password)
    l_id = Login.objects.get(user_name=username, password=password)
    request.session['login_id'] = l_id.id

    return redirect(user_dashboard)

def create_article(request):
    if request.session.get('login_id'):
        if request.method == 'POST':
            id = Article(uploaded_by= Login.objects.get(id = request.session.get('login_id')))
            form = ArticleForm(request.POST, request.FILES,instance=id)
            # print(form.data) # returns query dictionary

            if form.is_valid():
                form.save()
                return HttpResponse('Article Posted !!')
        else:
            form = ArticleForm()
            login_id = request.session.get('login_id')
            print("------",login_id)
            return render(request,'create_article.html',{'form': form,'login_id':login_id })
    else:
        return redirect('login')

""" TODO :  logout from user account,
            tags,
            show articles on index page by latest date
"""