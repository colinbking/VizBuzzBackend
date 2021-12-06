from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password
import uuid 

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, id, name, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not id:
            id = str(uuid.uuid4())
            raise ValueError(_('The id must be set'))
        if not name:
            raise ValueError(_('The name must be set'))
        if not username:
            raise ValueError(_('The username must be set'))
        if not password:
            raise ValueError(_('The password must be set'))

        user = self.model(id=id, name=name, username=username, password=password, **extra_fields)
        user.set_password(make_password(password))
        user.save()
        return user

    def create_superuser(self,username, password, id=None, name=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        if not id: id = str(uuid.uuid4())
        if not name: name = username
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        print("returning superuser: ", username)
        return self.create_user(id, name, username, password, **extra_fields)