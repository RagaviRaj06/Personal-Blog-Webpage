from typing import Any
# from django.core.management.base import BaseCommand
from blog.models import Category
 # BaseCommand is a class from django.core.management.base
from django.core.management.base import BaseCommand

#command to populate the database with dummy data
class Command(BaseCommand):
    help = "This commands inserts category data"
#function to handle the command
    def handle(self, *args: Any, **options: Any):
        #Delete
        Category.objects.all().delete()

        categories = ['Sports', 'Technology', 'Science', 'Art', 'Food']
        
        
        #for loop.
        for category_name in categories:
            Category.objects.create(name = category_name)
        #print a message to the console
        self.stdout.write(self.style.SUCCESS("Completed inserting Data!"))