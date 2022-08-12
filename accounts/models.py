from datetime import datetime
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager
    )

# Create your models here.

class UserManager(BaseUserManager):
    def createuser(self,email,password=None,is_admin=False,is_staff=False,is_active=True):
        if not email:
            raise ValueError('Email field is required')
        if not password:
            raise ValueError('Password field is required')
        # create the user instance
        user_obj = self.model(
            email = self.normalize_email(email)
            )
        user_obj.set_password(password)
        user_obj.staff =  is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        # save the created user
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self,email,password=None):
        '''create a staff user'''
        user = self.createuser(
            email,
            password = password,
            is_staff= True
            )
        return user

    def create_superuser(self,email,password=None):
        '''create a superuser'''
        user = self.createuser(
            email,
            password=password,
            is_staff = True,
            is_admin = True
        )

class User(AbstractBaseUser):
    '''change the default username field to email field'''
    email       = models.EmailField(verbose_name='Email:', blank=False,unique=True,max_length=255)
    full_name   = models.CharField(max_length=255,verbose_name='Full Name:',null=True,blank=True)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    confirmed   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #user get created and login using their email
    REQUIRED_FIELDS = [] # their full name is required to create user

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def get_full_name(self, *args,**kwargs) -> str:
        return self.full_name

    def get_short_name(self, *args, **kwargs) -> str:
        return self.full_name

    def has_perm(self, perms, obj = None) -> bool:
        return True
    
    def has_module_perms(self,app_label) -> bool:
        return True

    @property
    def is_staff(self, *args, **kwargs) -> bool:
        return self.staff
    
    @property
    def is_active(self, *args, **kwargs) -> bool:
        return self.active
    
    @property
    def is_admin(self, *args, **kwargs) -> bool:
        return self.admin

    def new_user(self, *args, **kwargs):
        '''
        @ return user joined in less than one week
        '''
        return self.confirmed and ((datetime.today() - 7) <= self.date_joined.date() <= (datetime.today()))

class UserProfile(models.Model):
    user        = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    profile_pic = models.ImageField(verbose_name='Profile Picture:',upload_to='profile_pictures/%y/%m/%d',null=True,blank=True)

    class Meta:
        managed = True
        verbose_name = 'ProfilePicture'
        verbose_name_plural = 'ProfilePictures'
    
    def __str__(self) -> str:
        return self.user.full_name