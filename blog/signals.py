#import group from auth_group & permissions
from django.contrib.auth.models import Group,Permission
#crate a group function
def create_groups_permissions(sender, **kwargs):
    #try to avoid function
    try:
        #create groups for readers using Group.objects.getor create- if the data is already there it will get or new it will create
        #readers_group  variable for get and created variable for create 
        readers_group,created = Group.objects.get_or_create(name="Readers")
        #create authors
        authors_group,created = Group.objects.get_or_create(name="Authors")
        editors_group,created = Group.objects.get_or_create(name="Editors")

        
        #create permissions
        readers_permissions = [
            Permission.objects.get(codename="view_post")
        ]

        authors_permissions = [
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post"),           
            Permission.objects.get(codename="view_post")
       ]
        #created a variable can_publish for get and created for create. This is to create codename in database
        can_publish,created = Permission.objects.get_or_create(codename="can_publish",content_type_id = 7, name="Can Publish Post")
        editors_permissions = [
            #can_publish variable called
            can_publish,
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post"),         
            Permission.objects.get(codename="view_post")
        ]

        #assiging the permissions to groups
        readers_group.permissions.set(readers_permissions)
        authors_group.permissions.set(authors_permissions)
        editors_group.permissions.set(editors_permissions)
        print("Groups and Permissions created Successfully")
#if error occured
    except Exception as e:
        print(f"An error occured{e}")

    
