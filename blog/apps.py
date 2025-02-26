from django.apps import AppConfig
#import post_migrate
from django.db.models.signals import post_migrate

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    #function for import signals and post migrate
    def ready(self):
        from blog.signals import create_groups_permissions
        post_migrate.connect(create_groups_permissions)