from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from . forms import NewsLetterForm, NewArticleForm, NewProfileForm
from . models import Article, NewsLetterRecipients
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile
# from . email import send_welcome_email
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from . models import MoringaMerch
# from . serializer import MerchSerializer
import datetime as dt
# from rest_framework import status
# from .permissions import IsAdminOrReadOnly



# Create your views here.
# class MerchList(APIView):
#     permission_classes =(IsAdminOrReadOnly,)
#     def get(self, request, format=None):
#         all_merch = MoringaMerch.objects.all()
#         serializers = MerchSerializer(all_merch, many=True)
#         return Response(serializers.data)
#
#     def post(self, request, format=None):
#         serializers = MerchSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # permission_classes = (IsAdminOrReadOnly,)

def welcome(request):
    return HttpResponse('Welcome to the Moringa Tribune')

# def news_of_day(request):
#     date = dt.date.today()
#
#     #Function to convert date object to find exact day
#     day = convert_dates(date)
#     html = f'''
#         <html>
#             <body>
#                 <h1>News for {day} {date.day}-{date.month}-{date.year} </h1>
#
#             </body>
#         </html>
#         '''
#     return HttpResponse(html)
@login_required(login_url='/accounts/register/')
def news_today(request):
    # date = dt.date.today()
    news = Article.objects.all()
    # form = NewsLetterForm()
    # if request.method == 'POST':
    #     form = NewsLetterForm(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data['your_name']
    #         email = form.cleaned_data['email']
    #         recipient = NewsLetterRecipients(name = name, email = email)
    #         recipient.save()
    #         send_welcome_email(name,email)
    #         HttpResponseRedirect('news_today')
    #
    # else:
    #     form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', { "news":news, })





# def convert_dates(dates):
#     #Function that gets the weekday number for the date.
#     day_number = dt.date.weekday(dates)
#
#     days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',"Sunday"]
#
#     #returning the actual dy of the week
#     day = days[day_number]
#     return day

# def past_days_news(request,past_date):
#     #Converts data from the string Url
#     date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

def past_days_news(request,past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
    except valueError:
        # Raise 404 error when valueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)

    return render(request, 'all-news/past-news.html', {"date": date,"news": news})


    # day = convert_dates(date)
    # html = f'''
    #     <html>
    #         <body>
    #             <h1>News for {day} {date.day}-{date.month}-{date.year}</h1>
    #         </body>
    #     </html>
    #         '''
    # return HttpResponse(html)

#Create your views here.

def welcome(request):
    return render(request, 'welcome.html')

def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_titles(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles":searched_articles})

    else:
        message = "You haven't searchred for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})


@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form =  NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
            return redirect('profile')
    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form":form})


@login_required(login_url='/accounts/login/')
def new_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form =  NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()

    else:
        form = NewProfileForm()
    return render(request, 'new_profile.html', {"form":form})


@login_required
def profile(request,user_id=None):
    if user_id==None:
        user_id=request.user.id
    # current_user = user_id
    user = User.objects.get(id = user_id)
    profile = user.profile
    images = Article.objects.filter(editor=user_id).order_by('-pub_date')
    # followers = len(Follow.objects.followers(user))
    # following = len(Follow.objects.following(user))
    post = len(Article.objects.filter(editor=user))
    return render(request, 'all-news/profile.html', {"images": images, 'user': request.user, "profile": profile, "posts":post})



def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')
    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

# @login_required
# def profile(request):
#     current_user = request.user.id
#     user = request.user
#     profile = Profile.objects.get(user=current_user)
#     images = Image.objects.filter(owner=current_user).order_by('-pub_date')
#     followers = len(Follow.objects.followers(user))
#     following = len(Follow.objects.following(user))
#     posts = len(Image.objects.filter(owner=user))
#     return render(request, 'profile.html', {"images": images, 'user': request.user, "profile": profile,"followers":followers,"following":following,"posts":posts})
#
