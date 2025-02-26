from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Category, Post

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email',  required=True)
    message = forms.CharField(label='Message',  required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=100, required=True)
    email = forms.CharField(label='email', max_length=100, required=True)
    password = forms.CharField(label='password', max_length=100, required=True)
    password_confirm = forms.CharField(label='password confirm', max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100, required=True)
    password = forms.CharField(label='password', max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No User Registered with this email.")
        
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', min_length=8)
    confirm_password = forms.CharField(label='Confirm Password', min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


#model form bcoz new data will add in database
class PostForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=200, required=True)
    content = forms.CharField(label="Content", required=True)
    #modelChoiceField used for already created model choice field from the model database we can choose the data
    #queryset is a collection of objects from your database
    category =  forms.ModelChoiceField(label='Category', required=True, queryset=Category.objects.all())
    #img url used to upload the image using imageField
    img_url = forms.ImageField(label='Image', required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img_url']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        

        #custom validation
        if title and len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 Characters long.')
        
        if content and len(content) < 10:
            raise forms.ValidationError('Content must be at least 10 Characters long.')
        #save function for img url get the data from view
    def save(self, commit = ...):
        #The super() function is used to give access to methods and properties of a parent or sibling class
        #To save changes to an object that's already in the database, use save()
        #Save this form's self.instance object if commit=True. Otherwise, add a save_m2m() method to the form which can be called after the instance is saved manually at a later time
        post = super().save(commit)
        #get the data from the img url
        cleaned_data = super().clean()
        #if cleaned data get the url then the img will reflect
        if cleaned_data.get('img_url'):
            post.img_url = cleaned_data.get('img_url')
        #else no image will reflect
        else:
            img_url ="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"
            # the post img url value assigned
            post.img_url = img_url
        # if commit true it will save the post data otherwise the commit false no img will reflect
        if commit:
            post.save()
        return post