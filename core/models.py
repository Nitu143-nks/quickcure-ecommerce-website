from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    phone_field = models.CharField(max_length=12, blank=False)

    def __str__(self):
        return self.user.username

# Category Model
class Category(models.Model):  # Fixed typo: "Catogory" -> "Category"
    category_name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.category_name

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(  # Fixed lazy reference to match correct model
        'Category',  # Referencing the correct `Category` model
        on_delete=models.CASCADE
    )
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    product_available_count = models.IntegerField(default=0)
    img = models.ImageField(upload_to='image/')
    def get_add_to_cart_url(self):
        # Fixed typo in `reverse` function and arguments
        from django.urls import reverse
        return reverse("core:add-to-cart", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        # Representing the object with a readable format
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        # Returns the total price for this item (price * quantity)
        return self.quantity * self.product.price

    def get_final_price(self):
        # This method is currently redundant but may be extended in the future
        return self.get_total_item_price()
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who placed the order
    items = models.ManyToManyField('OrderItem', related_name='orders')  # Related order items
    start_date = models.DateTimeField(auto_now_add=True)  # When the order was created
    ordered_date = models.DateTimeField(null=True, blank=True)  # When the order was finalized
    ordered = models.BooleanField(default=False)  # Whether the order has been placed
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Unique identifier for the order
    datetime_of_payment = models.DateTimeField(null=True, blank=True)  # Timestamp of payment
    order_delivered = models.BooleanField(default=False)  # Whether the order was delivered
    order_received = models.BooleanField(default=False)  # Whether the order was received by the customer
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)  # Razorpay-specific order ID
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)  # Razorpay payment ID
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)  # Razorpay payment signature

    def save(self, *args, **kwargs):
        # Automatically generate an order ID if it's not already set
        if not self.order_id and self.datetime_of_payment:
            self.order_id = self.datetime_of_payment.strftime('PAY2ME%Y%m%dODR') + str(self.pk or "")
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

    def get_total_price(self):
        # Calculate the total price of all items in the order
        return sum(order_item.get_final_price() for order_item in self.items.all())

    def get_total_count(self):
        # Get the total count of items in the order
        return sum(order_item.quantity for order_item in self.items.all())
    
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Make it optional
  # New field for mobile number
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)  # Optional if appropriate
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.mobile_number}"  # Updated string representation
    
from django.db import models
from django.urls import reverse

class Medicine(models.Model):  # Renaming for clarity
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        'Category',  # Refers to a Category model
        on_delete=models.CASCADE
    )
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    product_available_count = models.IntegerField(default=0)
    img = models.ImageField(upload_to='image/')
    expiration_date = models.DateField(null=True, blank=True)  # Optional
    manufacturer = models.CharField(max_length=255, null=True, blank=True)  # Optional
    prescription_required = models.BooleanField(default=False)  # Optional

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
    






        
       
