from django.db import models


class Customer(models.Model):
    email=models.EmailField()
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    password=models.CharField(max_length=128)
    mobile_no = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    username = models.CharField(max_length=150, unique=True, null=True)  

class Cake(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    name = models.CharField(max_length=100)
    flavour = models.CharField(max_length=10, default='Vanilla')
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    description = models.TextField()
    image = models.ImageField(upload_to='cakes/', null=True, blank=True)
    available = models.BooleanField(default=True)

    
class CakeCustomization(models.Model):
    message = models.TextField()
    egg_version = models.CharField(max_length=10)
    toppings = models.TextField()
    shape = models.TextField()
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cake = models.ManyToManyField(Cake, related_name='cart')
    quantity = models.PositiveIntegerField(default=1) 
    customization = models.ForeignKey(CakeCustomization, on_delete=models.CASCADE, null=True, default=None)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0) 


class Order(models.Model):
    Payment_method=[
        ('debit_card','Debit Card'),
        ('credit_card','Credit Card'),
        ('cash','Cash On Delivery'),
        ('unknown','Unknown')
    ]
    Payment_status=[
        ('pending','Pending'),
        ('paid','Paid'),
        ('cancelled','Cancelled')
    ]
    Order_status=[
        ('pending','Pending'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled')
    ]
        
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cake_customization = models.ForeignKey(CakeCustomization, on_delete=models.CASCADE, default=None,null=True,blank=True)
    items = models.ManyToManyField(Cart, related_name='order')
    quantity = models.PositiveIntegerField(default=0)  # PositiveIntegerField for quantity
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # DecimalField for total_price
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(max_length=225, default=None)
    order_status = models.CharField(max_length=50, choices=Order_status, default='pending')
    payment_status = models.CharField(max_length=50, choices=Payment_status, default='pending')
    payment_method = models.CharField(max_length=50, choices=Payment_method, default='unknown')





class Store(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name
