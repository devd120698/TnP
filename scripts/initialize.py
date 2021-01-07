import django
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

def run():
    # Create super user
    User.objects.create_superuser('superuser1', 'admin@portal.com', 'Wsdc@123')

    print("Superuser created...")

    # Create groups
    Group.objects.create(name='Student')
    Group.objects.create(name='Coordinator')
    Group.objects.create(name='Administrator')

    print("Groups created...")