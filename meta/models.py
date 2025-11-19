from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

import uuid


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password=None, legal_name="", greeting_name="", is_admin=False):
        if legal_name and not greeting_name:
            greeting_name = legal_name.split(" ")[0]

        user = self.model(email=self.normalize_email(email))
        user.legal_name = legal_name
        user.greeting_name = greeting_name
        user.set_password(password)
        if is_admin:
            if user.email != "root@localhost":
                raise ValueError("wrong e-mail for admin")

        user.save()
        return user

    def create_superuser(self, **kwargs):
        return self.create_user(**kwargs, is_admin=True)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    _rowid = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    email = models.EmailField(unique=True)
    legal_name = models.CharField(max_length=150, verbose_name="Name")
    greeting_name = models.CharField(max_length=100, verbose_name="Greeting")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['legal_name']

    objects = UserManager()

    def get_full_name(self):
        return self.legal_name

    def get_short_name(self):
        return self.greeting_name

    @property
    def is_superuser(self):
        return self.email == "root@localhost"

    @property
    def is_staff(self):
        return self.email.endswith("@localhost")
