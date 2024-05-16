from django.db import models
import datetime,os
from django.utils.html import mark_safe
from auths.models import User
# Create your models here.
def get_file_path(request, filename):
    original_filename =filename
    nowTime= datetime.datetime.now().strftime("%Y-%m-%d")
    filename= "%s.%s" % (nowTime,original_filename)
    return os.path.join('uploads/', filename)
STATUS_CHOICE={
    ('process','Processing'),
    ('shiped','shiped'),
    ('devlived','delived')
}
STATUS={
    ('draft','Draft'),
    ('disable','Disable'),
    ('rejected','Rejected'),
    ('in_review','In Review'),
    ('published','Published')
}
RATING={
    (1,'⭐✰✰✰✰'),
    (2,'⭐⭐✰✰✰'),
    (3,'⭐⭐⭐✰✰'),
    (4,'⭐⭐⭐⭐✰'),
    (5,'⭐⭐⭐⭐⭐')
}
class Tag(models.Model):
    tag= models.CharField(max_length=100)
    def __str__(self):
        return self.tag
# Create your models here.
class Category(models.Model):
    slug= models.CharField(max_length=150, null= False,blank=False)
    name= models.CharField(max_length=150, null= False, blank=False)
    image= models.ImageField(upload_to=
                             get_file_path,null= True, blank=True)
    desc= models.TextField(max_length=500, null=True, blank=True)
    status= models.BooleanField(default=False,help_text="0=default, 1=Hidden")
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    slug= models.CharField(max_length=150, null= False,blank=False)
    name= models.CharField(max_length=150, null= False, blank=False)
    image= models.ImageField(upload_to=get_file_path,null= True, blank=True)
    desc= models.TextField(max_length=500, null=True, blank=True)
    status=  models.BooleanField(default=False,help_text="0=default, 1=Hidden")
    quantity= models.IntegerField(null=False,blank=False)
    price= models.FloatField(null=False,blank=False)
    sell_price= models.FloatField(null=False,blank=False)
    tags= models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    in_stock= models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def get_image(self):
        return mark_safe('<img src="%s" width= "50" height="50"/>' % (self.image.url))
    def get_percentage(self):
        new_price= (self.sell_price/self.price)*100
        return new_price
class ProductReview(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    review= models.TextField()
    rating= models.IntegerField(choices=RATING,default=None)
    status = models.BooleanField(default=True)
    date= models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Products Review"

    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.rating
class Contact(models.Model):
   name= models.CharField(max_length=155, null=True)
   email= models.CharField(max_length=155, null=True)
   phone= models.CharField(max_length=155, null=True)
   message= models.TextField()
#    status= models.BooleanField(default=True)
   answer= models.TextField()

class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    qty= models.IntegerField(null=False, blank=False)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name
    
class Whishlist(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)

    date= models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Whishlist"

    def __str__(self):
        return self.product.title
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     fname= models.CharField(max_length=150, null=False)
#     lname=models.CharField(max_length=150, null=False)
#     email= models.CharField(max_length=150, null=False)
#     phone= models.CharField(max_length=150, null=False)
#     address= models.TextField()
#     city=models.CharField(max_length=150, null=False)
#     state= models.CharField(max_length=150, null=False)
#     country= models.CharField(max_length=150, null=False)
#     pincode= models.CharField(max_length=150, null=False)
#     payment_mode= models.CharField(max_length=150, null=False)
#     payment_id= models.CharField(max_length=250, null=True) 
#     status= models.CharField(choices=STATUS_CHOICE, default='Processing')
#     message= models.TextField()
#     tracking_no= models.CharField(max_length=150, null=True)
#     created_at= models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
# class OrderItem(models.Model):
#     order= models.ForeignKey(Order, on_delete=models.CASCADE)
#     product= models.ForeignKey(Product, on_delete=models.CASCADE)
#     price= models.FloatField(null=False)
#     quantity= models.IntegerField(null=False)

#     def __str__(self):
#         return '{} {}'.format(self.order.id, self.order.tracking_no)