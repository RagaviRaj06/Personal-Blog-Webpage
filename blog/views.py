from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
import logging
#to import for models
from .models import Category, Post, AboutUs
#import for exception handling
from django.http import Http404 
#to import for pagination
from django.core.paginator import Paginator
 #importing forms module from django
from .forms import ContactForm, ForgotPasswordForm, PostForm, RegisterForm, LoginForm, ResetPasswordForm
#message module
from django.contrib import messages
#to import authenticate and login as auth_login
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
#import forms
from blog import forms
#import user
from django.contrib.auth.models import User
#token generator
from django.contrib.auth.tokens import default_token_generator
#import urlsafe base64 encode- trying to pass a user ID (primary key) to url as base 64 encoded
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#import force_bytes() will convert the given int to str and then convert that str to bytes.
from django.utils.encoding import force_bytes
#import Check if contrib.sites is installed and return either the current Site object or a RequestSite object based on the request.
from django.contrib.sites.shortcuts import get_current_site
#import Load a template and render it with a context. Return a string.
from django.template.loader import render_to_string
#sending an Email
from django.core.mail import send_mail
#import decorators for loginrequired
from django.contrib.auth.decorators import login_required, permission_required
#import models groups
from django.contrib.auth.models import Group


# Create your views here.
#posts=[
 #       {"id":1, "title":"Post 1", "content":"This is the first post"},
 #       {"id":2, "title":"Post 2", "content":"This is the second post"},
  #      {"id":3, "title":"Post 3", "content":"This is the third post"},
   #     {"id":4, "title":"Post 4", "content":"This is the fourth post"},
   # ]

def index(request):
    #variable interpolation
    blog_title="Latest Posts"
    #getting data from all post model
    #all_posts = Post.objects.all()
    #getting data from post model using filter
    all_posts = Post.objects.filter(is_published=True)
    #pagination
    #paginator to assign all posts and number of posts to be displayed
    paginator = Paginator(all_posts, 5)
    #getting page number from request
    page_number = request.GET.get('page')
    #getting posts from paginator
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/index.html",  {'blog_title': blog_title , 'page_obj': page_obj})#variable interpolation

def detail(request, slug):
    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request,'You have no permission to view any post!')
        return redirect('blog:index')

    #static data
    #post = next((item for item in posts if item["id"] == int(post_id)), None)
    #handling exception
    try:
        #getting data from post model using id from database
        #post = Post.objects.get(pk=post_id)

        #getting data from post model using slug from database
        post = Post.objects.get(slug=slug)
        #getting related posts
        related_post = Post.objects.filter(category = post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("Post Does Not Exist")
    #logger = logging.getLogger("TESTING")
    #logger.debug(f"post variable is {post}")
    return render(request,"blog/detail.html", {'post':post , 'related_posts':related_post})

def old_url_redirect(request):
    return redirect(reverse("blog:new_url_id"))

def new_url_view(request):
    return HttpResponse("This is the new URL")

def contact(request):
    #getting data from the form
    #if request == submit then get the data from the form
    if request.method == "POST":
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        #logging
        logger = logging.getLogger("TESTING")
        #logger.debug(f"post data is {name} {email} {message}")
        #if form is valid then get the data from the form
        if form.is_valid():
            logger.debug(f"post data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}")
            #success message
            success_message = "Form submitted successfully"
            return render(request,"blog/contact.html",{'form':form, 'success_message':success_message})
        else:
            logger.debug("Form is invalid")
            #error message
        return render(request,"blog/contact.html",{'form':form, 'name':name, 'email':email, 'message':message})
    return render(request,"blog/contact.html")

def about(request):
    #getting data from the about us model in admin page as a dynamic content
    about_content=AboutUs.objects.first().content
    return render(request, "blog/about.html",{'about_content':about_content})

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            #while saving user data it will commit false 
            user = form.save(commit = False) #user data creation
            #set_password method is used to hash the password(inbuilt method) -> getting data using cleaned_data method and get the value of password
            user.set_password(form.cleaned_data["password"])
            #save the data in database
            user.save()
            #get or create from the name Readers
            readers_group,created = Group.objects.get_or_create(name="Readers")
            #users will get add under the readers group
            user.groups.add(readers_group)
            #messages.success method is used to display the message
            messages.success(request,"Registration Successful. You can login!!")  
            return redirect("blog:login")       
    return render(request, "blog/register.html", {'form':form})

def login(request):
    form = LoginForm()
    if request.method == "POST":
        #loginform
        form = LoginForm(request.POST)
        #if form is valid
        if form.is_valid():
            #get data from cleaned_data dictionary
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            # it authenticate from the database
            user = authenticate(username=username, password=password)
            #if user values is not none then
            if user is not None:
                #login request of the user
                auth_login(request, user)
                #redirect to the dashboard page
                return redirect("blog:dashboard")
                #it prints the value
                print("Login Successfully")
    return render(request, "blog/login.html", {'form':form})

def dashboard(request):
    blog_title ="My Posts"
     #getting data from all post model
    all_posts=Post.objects.filter(user=request.user)
    #paginator to assign all posts and number of posts to be displayed
    paginator = Paginator(all_posts, 5)
    #getting page number from request
    page_number = request.GET.get('page')
    #getting posts from paginator
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/dashboard.html',{"blog_title":blog_title, 'page_obj':page_obj})

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send email to reset password
            #used to create a default token for the user
            token = default_token_generator.make_token(user)
            #urlsafe_base64 - Encode a bytestring to a base64 string for use in URLs
            #forcebyte-convert string into the bytes using primary key as per the user
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            #get current site data like http://127.0.0.1:8000/
            current_site = get_current_site(request)
            #to get the data from template and display in domain http://127.0.0.1:8000/
            domain = current_site.domain
            subject = "Reset Password Requested"
            #get the message from template
            #render to string - convert to string
            message = render_to_string('blog/reset_password_email.html',{
                'domain': domain,
                #base 64
                'uid': uid,
                #primary token id
                'token': token
            })
            #sending an email(subject, message, from-mail,recipent list whom want to receive email)
            send_mail(subject, message, 'noreply@gmail.com', [email])
            messages.success(request,"Email has been sent")

    return render(request,"blog/forgot_password.html", {'form':form})


def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
     #if request == submit then get the data from the form
    if request.method == 'POST':
        #form
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('blog:login')
            else :
                messages.error(request,'The password reset link is invalid')

    return render(request,'blog/reset_password.html', {'form': form})

#Decorator for views that checks that the user is logged in, redirecting to the log-in page if necessary.
@login_required
@permission_required('blog.add_post',raise_exception=True)
def new_post(request):
    #get all category using category.objects.all from database
    categories = Category.objects.all()
    form = PostForm()
    if request.method == "POST":
        #form
        #request.files = use to upload the files data
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            #commit: false it will return an object that hasn't yet been saved to the database
            post = form.save(commit=False)
            #post user is assigned in the model for the created post in dashboard so getting data from database 
            # get the user data from request
            post.user = request.user
            #save the post 
            post.save()
            return redirect('blog:dashboard')
    return render(request,'blog/new_post.html', {'categories': categories, 'form': form})

@login_required
@permission_required('blog.change_post',raise_exception=True)
def edit_post(request, post_id):
    categories = Category.objects.all()
    #Use get() to return an object, or raise an Http404 exception if the object does not exist.
    post = get_object_or_404(Post, id=post_id)
    form = PostForm()
    if request.method =="POST":
        #form = request.send post data , #request.files = send/upload the files data, 
        #instance = sending already existing data to the form[A Form instance is either bound to a set of data, or unbound]
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            #<!--included post updated msg -->
            messages.success(request,'Post Updated Successfully')
            return redirect('blog:dashboard')
    return render(request, 'blog/edit_post.html', {'categories': categories,'post':post,'form':form})

@login_required
@permission_required('blog.delete_post',raise_exception=True)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    #post delete method is used to delete the post
    post.delete()
    messages.success(request, 'Post Deleted Succesfully!')
    return redirect('blog:dashboard')

@login_required
@permission_required('blog.can_publish',raise_exception=True)
def publish_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    #is_published = True method is used to publish the data
    post.is_published = True
    post.save()
    messages.success(request, 'Post Published Succesfully!')
    return redirect('blog:dashboard')