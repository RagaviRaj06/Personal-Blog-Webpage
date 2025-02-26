from django.db import models
#to import for slug
from django.utils.text import slugify
from django.contrib.auth.models import User

#category model  
class Category(models.Model):
    name = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    #ImageField is used to upload the image, upload_to = where the images want to store"
    img_url = models.ImageField(null=True, upload_to="posts/images")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    #to add many to one category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #add the user for the created post in dashboard so getting data from database
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #if user added a new post if they want to publish it then only it want to reflect in page
    #its an boolean field should defaultly be false if they give publish then only it want to true and reflect
    is_published = models.BooleanField(default=False)

#to generate slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    #returns a special descriptor object which allows direct access to getter, setter, and deleter methods
    @property
    def formatted_img_url(self):
        url = self.img_url if self.img_url.__str__().startswith(('http://','https://')) else self.img_url.url
        return url


    def __str__(self):
        return self.title

class AboutUs(models.Model):
    content = models.TextField()