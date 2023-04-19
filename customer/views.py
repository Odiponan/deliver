from django.views import View
from django.shortcuts import render
from django.forms import EmailField
from django.core.mail import send_mail
from django.template import RequestContext
from .models import MenuItem, OrderModel

class Index(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'customer/index.html')



def index(request):
    customers = Customer.objects.all()
    return render(request, 'customer/index.html', {'customers': customers})

    
class About(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request):
        price = 0

        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        entrees = MenuItem.objects.filter(category__name__contains='Entre')

        # pass into context
        context = {
            'appetizers': appetizers,
            'drinks': drinks,
            'desserts': desserts,
            'entres': entres,
        }

        # render the template
        return render(request, 'customer.html',context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        
        order_items = {'items': []}
        item_ids = []
        price = 0
        
        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            price += item_data['price']
            order_items['items'].append(item_data)
            item_ids.append(item_data['id'])
            
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )

        order.items.add(*item_ids)

        # send confirmation email to the user
        body = f'Thank you for your order, your food is being made and will be delivered!\nYour total: {price}\nThank you again for your order'
        send_mail('Thank You For Your Order', body, email, [email], fail_silently=False)

        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items.all(),
            'price': order.price
        }

        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        date = json.loads(request.body)

        if date['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render
        
class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
        
class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q") 

        menu_item = MenuItem.objects.filter(
            Q(name__icontains=query),
            Q(price__icontains=query),
            Q(description__icontains=query)
        )
        menu_items = ['drinks', 'appetizers', 'entres', 'desserts' ]
        context = { 
            'menu_items': menu_items 
        }
        return render(request, 'customer/menu.html', context)
