import random

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from article_app.models import Users,Login,Article , Article_Tags,Tags , Post_Category
from datetime import datetime
from .forms import ArticleForm ,TagsForm
from twilio.rest import Client
from django.core import exceptions
# from django.contrib.auth import logout
# Create your views here.


def index(request):
    articles = Article.objects.order_by('-uploaded_on')
    return render(request,'index.html',{'articles':articles})

def checkusername(request):
    username = request.POST.get('username')
    user = Users.objects.filter(username = username)

    if user :
        return HttpResponse('Username is already taken')
    else:
        return HttpResponse("Username is available")
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
    return redirect(login)


def user_dashboard(request):
    if request.session.get('login_id') is not None:
        l_id = int(request.session.get('login_id'))
        Name = Users.objects.get(login_id=l_id).name
        request.session['name'] = Name
        articles = Article.objects.order_by('-uploaded_on')
        return render(request,'user_Dashboard.html',{'articles':articles})
    else :
        return redirect(login)

def logout_act(request):
    request.session.clear()
    return redirect(index)


def login(request):
    return render(request,'login.html')


def getlogin(request):
    username= request.POST.get('username')
    password = request.POST.get('password')
    # print(username ,"       ",password)
    try:
        l_id = Login.objects.get(user_name=username, password=password)
        request.session['login_id'] = l_id.id
    except :
        return render(request,'login.html',{'error': "Username or Password Incorrect" })

    return redirect(user_dashboard)


def forget_password(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = random.randint(1000,9999)
        request.session['otp'] = str(otp)
        request.session['mobile'] = mobile
        print(otp)
        try:
            check_mobile = Users.objects.get(mobile=mobile)
            #Your new Phone Number is +15205953157
            account = "ACa116d5c31df01d9700df67da9b8af7de"
            token = "2f16bfeb36ec80122c202cfd5c84c248"
            client = Client(account, token)
            message = client.messages.create(
                body="Your otp for password reset is :"+str(otp),
                from_= "+15205953157",
                to= "9998090056"
            )
            print(message.sid)
            msg = "Otp sent to registered mobile number."
            return render(request,'validate_otp.html',{'msg':msg})
        except :

            msg = "This mobile number is not registered."
            return render(request,'forget.html',{'message':msg})
    else:
        return render(request,'forget.html')

def validate_otp(request):
    sent_otp = request.session.get('otp')
    received_otp = request.POST.get('otp')
    print(sent_otp)
    if sent_otp == received_otp :
        return redirect('change_password')
    else:
        msg = "OTP is not matched, Please enter valid OTP"
        return render(request, 'validate_otp.html', {'error': msg})

def change_password(request):
    if request.method == 'POST':
        mobile = request.session.get('mobile')
        print(mobile)
        password = request.POST.get('pass')
        user = Users.objects.filter(mobile= mobile).first()
        print(user)
        user.password = password
        user.save()
        return HttpResponse("Password changed successfully.."
                            '<html>'
                            '<body>'
                            '<br>'
                            '<a href = "/ ">Go to Home</a>'
                            '</body>'
                            '</html>'
                            )
    else:
        return render(request,'change_password.html')






def create_article(request):
    if request.session.get('login_id'):
        if request.method == 'POST':
            id = Article(uploaded_by= Users.objects.get(id = request.session.get('login_id')))
            form = ArticleForm(request.POST, request.FILES,instance=id)
            tags_form = TagsForm(request.POST)

            print("form data :",form.data) # returns query dictionary

            print(tags_form.data['tags_title'])
            if form.is_valid() and tags_form.is_valid():
                form.save()
                tags_form.save()
                tag_id = Tags.objects.latest('id') # getting last row id
                print(tag_id.id)
                article_id = Article.objects.latest('id')
                print(article_id)
                article_tags_mapping = Article_Tags.objects.create(tags = tag_id , article = article_id)
            return HttpResponse('Article Posted !!\n'
                                '<html>'
                                '<body>'
                                '<br>'
                                '<a href = "user_dashboard">Go to Home</a>'
                                '</body>'
                                '</html>')
        else:
            form = ArticleForm()
            tags_form = TagsForm()
            login_id = request.session.get('login_id')
            print("------",login_id)
            return render(request,'create_article.html',{'form': form,'tags_form': tags_form ,'login_id':login_id })
    else:
        return redirect('login')


def update_profile(request):
    if request.session.get('login_id') is not None:
        if request.method == 'POST':
            print(request.body)
            id = request.POST.get('userid')
            print(id)
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            username = request.POST.get('username')
            date_of_birth = request.POST.get('dob')

            print(date_of_birth)
            userdata = Users.objects.get(id = id)
            userdata.name = name
            userdata.mobile = mobile
            userdata.username = username

            if date_of_birth :
                userdata.DOB = date_of_birth

            userdata.save()
            return render(request,'profile.html',{'userdata':userdata})
        else :
            user_data = Users.objects.filter(login_id = request.session.get('login_id')).first()
            print(user_data)
            return render(request,'profile.html',{'userdata':user_data})
    else:
        return redirect(login)

def show_post(request):
    id = request.GET.get('postid')
    article = Article.objects.filter(id = id).first()
    return render(request,'post.html',{'article':article})


def categorical_post(request):
    if request.session.get('login_id') is not None:
        category_id =  request.GET.get('category_id')
        category = Post_Category.objects.get(id= category_id)

        articles = Article.objects.filter(type=category).order_by('-uploaded_on')
        print(articles)
        if articles :
            return render(request,'user_Dashboard.html',{'articles':articles})
        else:
            return render(request, 'user_Dashboard.html', {'message': 'Sorry No post available !!'})
    else:
        category_id = request.GET.get('category_id')
        category = Post_Category.objects.get(id=category_id)

        articles = Article.objects.filter(type=category).order_by('-uploaded_on')
        print(articles)
        if articles:
            return render(request, 'index.html', {'articles': articles})
        else:
            return render(request, 'index.html', {'message': 'Sorry No post available !!'})
        return redirect(login)

def search_post (request): # showing post by search

    search = request.GET.get('search')
    all_tags_id = Tags.objects.filter(tags_title__icontains=search)
    if len(all_tags_id) == 0 :
        return render(request,'search_post.html',{'message':"Sorry ! No articles related your search "})
    else:
        print("all tags id :",all_tags_id)
        articles= []
        for tag_id in all_tags_id:
            article_tags_id = Article_Tags.objects.get(tags=tag_id)
            print("article id from article_tags table:",article_tags_id.article.id)
            article_post = Article.objects.filter(id=article_tags_id.article.id)
            print(article_post)
            articles.append(article_post)
        print(articles)
        return render(request,'search_post.html',{'articles':articles})
