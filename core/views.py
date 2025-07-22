from django.shortcuts import render,redirect,get_object_or_404
from core.forms import *
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from core.models import Product, Order, OrderItem, CheckoutAddress
from django.conf import settings



# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products': products})
def shop(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'core/shop.html', {'products': products})

def about(request):
    return render(request, 'core/about.html')
def contact(request):
    return render(request, 'core/contact.html') 
def cart(request, pk):
    # Redirect to login if the user is not authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to add items to your cart.")
        return redirect('logn')  # Redirect to the login page (using the 'logn' URL name)

    # Get the specific product
    product = get_object_or_404(Product, pk=pk)

    # Create or get an OrderItem for the product and the user
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
        defaults={'quantity': 1}  # Set the default quantity to 1 when creating a new item
    )

    # Get the active order for the user (not yet completed)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        # Retrieve the active order
        order = order_qs.first()
        # Check if the product is already in the order
        if order.items.filter(pk=order_item.pk).exists():
            # Increase the quantity of the product in the cart
            order_item.quantity += 1
            order_item.save()  # Make sure to save the updated quantity
            messages.info(request, f"Increased the quantity of {product.name} to {order_item.quantity}.")
        else:
            # Add the new product to the cart
            order.items.add(order_item)
            messages.info(request, f"Added {product.name} to your cart.")
    else:
        # Create a new order if none exists
        ordered_date = now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, f"Added {product.name} to your cart in a new order.")

    # Redirect to the product detail page
    return redirect("shop_single", pk=pk)
def shop_single(request, pk):
    # Use get_object_or_404 for better error handling
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/shop-single.html', {'product': product})
def search(request):
    # Logic for search
    return render(request, 'search.html')
def home(request):
    return render(request, 'home.html')
from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import CheckoutAddress

def checkout(request):
    # Check if the user already has a saved checkout address
    if request.user.is_authenticated and CheckoutAddress.objects.filter(user=request.user).exists():
        # If the user has a saved address, render the checkout page with "payment_allow"
        return render(request, 'core/checkout.html', {'payment_allow': "allow"})

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip')
            mobile_number = form.cleaned_data.get('mobile_number')

            # Create and save the checkout address
            CheckoutAddress.objects.create(
                user=request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip_code=zip_code,
                mobile_number=mobile_number
            )
            # After successful form submission, redirect to a summary or payment page
            return redirect('checkout')  # Redirect to another page after saving the data.

    else:
        # Initialize an empty form for GET requests
        form = CheckoutForm()

    # Render the checkout page with the form (if it's a GET request or a failed POST)
    return render(request, 'core/checkout.html', {'form': form})

def thank_you(request):
    return render(request, 'core/thankyou.html')
def register(request):
    return render(request, 'accounts/regis.html')
def login_v(request):
    return render(request, 'accounts/logn.html')
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('index')  # Redirect to the 'index' view (ensure it's correctly defined in urls.py)
        else:
            # If form is invalid, provide error messages
            messages.error(request, 'There was an error with your form submission. Please check the fields.')
    else:
        form = ProductForm()
    
    return render(request, 'core/add_product.html', {'form': form})

from django.shortcuts import redirect

def orderlist(request):
    if not request.user.is_authenticated:
        return redirect("logn")  # Redirect to login if the user is not logged in

    # Check if there's an active order for the user
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        items = order.items.all()  # Get all OrderItems in the order

        if request.method == 'POST':
            # Handle quantity update
            if 'update_quantity' in request.POST:
                item_id = request.POST.get('item_id')
                quantity = int(request.POST.get('quantity', 1))
                order_item = OrderItem.objects.get(id=item_id, user=request.user, ordered=False)
                order_item.quantity = max(1, quantity)  # Ensure quantity is at least 1
                order_item.save()
                return redirect('orderlist')  # Reload the page

            # Handle item removal
            if 'remove_item' in request.POST:
                item_id = request.POST.get('item_id')
                order_item = OrderItem.objects.get(id=item_id, user=request.user, ordered=False)
                order_item.delete()
                return redirect('orderlist')  # Reload the page

        total_price = order.get_total_price()  # Total price of the order
        return render(request, 'core/orderlist.html', {'order': order, 'items': items, 'total_price': total_price})

    # If no order exists
    return render(request, 'core/orderlist.html', {'message': "Your Cart is Empty"})

import razorpay
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, CheckoutAddress

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))


def payment(request):
    try:
        # Fetch the user's current order
        order = Order.objects.get(user=request.user, ordered=False)
        address = CheckoutAddress.objects.get(user=request.user)

        # Calculate order details
        order_amount = int(order.get_total_price() * 100)  # Convert to paisa
        order_currency = "INR"
        order_receipt = order.order_id

        # Create notes with address details
        notes = {
            "street_address": address.street_address,
            "apartment_address": address.apartment_address,
            "country": address.country.name,
            "zip": address.zip_code,
        }

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create(
            {
                "amount": order_amount,
                "currency": order_currency,
                "receipt": order_receipt,
                "notes": notes,
                "payment_capture": "0",  # Payment capture is manual
            }
        )

        # Save Razorpay order ID in the database
        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        # Render payment summary page
        return render(
            request,
            "core/paymentsummaryrazorpay.html",
            {
                "order": order,
                "order_id": razorpay_order["id"],
                "orderId": order.order_id,
                "final_price": order_amount / 100,  # Convert back to rupees
                "razorpay_merchant_id": settings.RAZORPAY_ID,
            },
        )
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)
    except CheckoutAddress.DoesNotExist:
        return HttpResponse("Address not found", status=404)
    except Exception as e:
        print(f"Error in payment view: {e}")
        return HttpResponse("An error occurred", status=500)
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
import razorpay

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            # Fetch Razorpay payment details
            payment_id = request.POST.get("razorpay_payment_id")
            order_id = request.POST.get("razorpay_order_id")
            signature = request.POST.get("razorpay_signature")

            if not (payment_id and order_id and signature):
                return HttpResponse("Missing payment details", status=400)

            # Verify payment signature
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # If successful, redirect to thankyou page
            return render(request, "thankyou.html", {"payment_id": payment_id})

        except razorpay.errors.SignatureVerificationError:
            return render(request, "paymentfailed.html", {"error": "Invalid signature"})
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return HttpResponse("Invalid request method", status=400)

    
def search_results(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(name__icontains=query) if query else None

    print("Query:", query)  # Debugging
    print("Medicines:", medicines)  # Debugging

    context = {
        'query': query,
        'medicines': medicines,
        'search_performed': bool(query),
    }
    return render(request, 'core/search_results.html', context)


