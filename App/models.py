from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class Product(models.Model):

    product_name = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9?!,.\s]+$',
                message="Product name can only contain letters, numbers, spaces, ?, !, and , characters."
            )
        ]
        )
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="product/images",default="")

    def __str__(self):
        return self.product_name

    def get_product_price(self):
        return self.price

class CartItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    price = models.IntegerField(default=False)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Orders(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    full_name = models.CharField(max_length=100,blank=False)
    country = models.CharField(max_length=100,blank=False)
    address = models.TextField(max_length=100,blank=False)
    city = models.CharField(max_length=100,blank=False)
    state = models.CharField(max_length=100,blank=False)
    pincode = models.CharField(max_length=100,blank=False)
    phone = models.IntegerField(blank=False)
    email = models.EmailField(max_length=100,blank=False)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    orders = models.ForeignKey(CartItems,on_delete=models.SET_NULL,null=True,blank=False)

    def __str__(self):
        return f"{self.full_name}"

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    message = models.TextField()

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("user must have an email address")

        user = self.model(
                email=self.normalize_email(email),
                password=password
                )

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email,password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=255,default=False)
    phone = models.IntegerField(default=False)
    email = models.EmailField(
        verbose_name="email address",
        max_length=50,
        unique=True
    )
    password=models.CharField(max_length=20)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Review(models.Model):
    name = models.CharField(max_length=100,default=True,blank=False)
    email = models.EmailField(max_length=100,default=True,blank=False)
    reviews = models.TextField(max_length=400,default=True,blank=False)
    rating = models.IntegerField(null=False, blank=False)
    product_name = models.CharField(max_length=255,default=True,null=False,blank=False)