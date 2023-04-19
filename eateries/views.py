from django.shortcuts import render, redirect
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_text


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the correct date
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.price
            if not order.is_shipped:
                unshipped_orders.append(order)
        # pass total number of orders and total number of revenues into the template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }
        return render(request, 'eateries/dashboard.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()
        context = {
            'order': order
        }
        return render(request, 'eateries/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }
        return render(request, 'eateries/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()
from django.shortcuts import render
from django.views import View

class OrderView(View):
    def get(self, request):
        # Handle GET request
        return render(request, 'order.html')

    def post(self, request):
        # Handle POST request
        return render(request, 'order.html')

       


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


def home(request):
    return render(request, "eateries/index.html")


def signUp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('home')


            # Validate user data
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        
        # Create user object
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        # Send confirmation email
        uidb64 = urlsafe_base64_encode(force_bytes(myuser.pk))
        token = account_activation_token.make_token(myuser)
        activate_url = f"{request.scheme}://{request.get_host()}/activate/{uidb64}/{token}/"
        message = render_to_string('email_confirmation.html', {'activate_url': activate_url})
        email = EmailMessage(
            "Confirm your email at eateries60@gmail.com",
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.send(fail_silently=True)
        
        # Show success message and redirect to home page
        messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email please confirm your email to activate your account.")
        return redirect('home')
    
    # Render sign up form
    return render(request, "signup.html")

def signIn(request):
    if request.method == "POST":
        # Extract user data from form
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Login user and redirect to index page
            login(request, user)
            fname = user.first_name
            return render(request, "index.html", {'fname': fname})
        else:
            # Show error message and redirect to login page
            messages.error(request, "Bad Credentials")
            return redirect('login')
    
    # Render login form
    return render(request, "login.html")

def signOut(request):
    # Log out user and redirect to home page
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and account_activation_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')






