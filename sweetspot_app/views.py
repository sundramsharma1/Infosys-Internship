from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import action
from django.utils import timezone
import sched,time,threading
from threading import Thread
from django.utils.timezone import now
from datetime import datetime,timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Customer, Cake, CakeCustomization, Cart, Order,Store
from .serializers import CustomerSerializer, CakeSerializer, CakeCustomizationSerializer, CartSerializer, OrderSerializer,StoreSerializer
import googlemaps

scheduler = sched.scheduler(time.time, time.sleep)

def run_scheduler():
    while True:
        scheduler.run(blocking=False)
        time.sleep(1)


Thread(target=run_scheduler, daemon = True).start()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            try:
                user = Customer.objects.get(email=email)
                if check_password(password, user.password):
                    # Add customer_id to the response
                    return Response({
                        "message": "Login Successful",
                        "customer_id": user.id, 
                        "username": user.username 
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except Customer.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Missing email or password"}, status=status.HTTP_400_BAD_REQUEST)
        
class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

class CakeCustomizationViewSet(viewsets.ModelViewSet):
    queryset = CakeCustomization.objects.all()
    serializer_class = CakeCustomizationSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class AddCakeToCartViewSet(viewsets.ViewSet):
    def create(self, request,pk=None):
        # Extract data from request
        customer_id = request.data.get('customer')
        cake_id = request.data.get('cake')
        quantity = request.data.get('quantity')
        customization_id= request.data.get('customization')

        try:
            # Check if customer exists
            customer = Customer.objects.get(id=customer_id)
            if not customer:
                return Response({"message": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if cake exists and is available
            cake = Cake.objects.get(id=cake_id)
            if not cake or not cake.available:
                return Response({"message": "Cake not found or not available"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if cake customization exists and is valid for the specified cake and customer
            if customization_id:
                customization = CakeCustomization.objects.filter(id=customization_id, customer=customer, cake=cake).first()
                if not customization:
                    return Response({"message": "Invalid cake customization"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if cart item already exists
            cart_item = Cart.objects.filter(customer=customer, cake=cake).first()
            if cart_item:
                # Update existing cart item
                cart_item.quantity = quantity
                cart_item.total_amount = cake.price * int(quantity)
                if customization_id:
                    cart_item.customization = customization
                cart_item.save()
                serializer = CartSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Create new cart item
                cart = Cart.objects.create(customer=customer, quantity=quantity, total_amount=cake.price * int(quantity))
                cart.cake.add(cake)
                if customization_id:
                    cart.customization = customization
                cart.save()
                serializer = CartSerializer(cart)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cake.DoesNotExist:
            return Response({"message": "Cake not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def update(self, request, pk=None):
        return self.create(request)
    def destroy(self, request, pk=None):
        try:
            # Fetch the cart item using its primary key
            cart_item = Cart.objects.get(pk=pk)
            cart_item.delete()
            return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"message": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def validate_card(self, card_number, expiry_date, cvv):
        print('1')
        # Validate card number format
        if not card_number.isdigit() or len(card_number) != 16:
            return False
        print('2')
        # Validate expiry date format 
        if len(expiry_date) != 7 or not expiry_date[:2].isdigit() or not expiry_date[3:].isdigit():
            return False
        print('3')
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Parse the expiry date string
        try:
            exp_month, exp_year = map(int, expiry_date.split('/'))
        except ValueError:
            return False
        print(current_month,current_year,exp_month, exp_year)
        # Check if the expiry year is in the past or the current year
        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            return False
        print('5')
        # Validate CVV format
        if not cvv.isdigit() or len(cvv) != 3:
            return False
        print('6')
        return True

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customer')
        cake_id = request.data.get('cake')
        delivery_address = request.data.get('delivery_address')

        try:
            # Validate customer
            customer = Customer.objects.get(id=customer_id)
            if not customer:
                return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

            # Validate cake
            cake = Cake.objects.filter(id=cake_id, available=True).first()
            if not cake:
                return Response({"message": "Cake not found or not available"}, status=status.HTTP_404_NOT_FOUND)
            
            

            # Fetch cart record for the customer and cake
            cart_item = Cart.objects.filter(customer=customer, cake=cake).first()
            if not cart_item:
                return Response({"message": "Cart item not found for the specified customer and cake"}, status=status.HTTP_404_NOT_FOUND)

            # Validate cart record
            if cart_item.quantity <= 0:
                return Response({"message": "Invalid quantity in cart item"}, status=status.HTTP_400_BAD_REQUEST)

            # Create order instance
            order = Order.objects.create(customer=customer, delivery_address=delivery_address)
            
            # Add cart item to order items
            order.items.add(cart_item)

            # Set order fields
            order.quantity = cart_item.quantity
            if cart_item.customization:
                order.cake_customization = cart_item.customization
            order.total_price = cart_item.total_amount

            order.save()

            # Serialize and return order
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

        except Customer.DoesNotExist:
            return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cake.DoesNotExist:
            return Response({"message": "Cake not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        

    def partial_update(self, request, pk=None):
        # Fetch the order instance from the order id in the URL
        order_id =pk
        order_instance = Order.objects.get(id=order_id)

        # Check if the order instance is valid
        if not order_instance:
            return Response({"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Get input fields from the request
        customer_id = request.data.get('customer_id')
        cake_id = request.data.get('cake_id')
        payment_method = request.data.get('payment_method')
        card_number = request.data.get('card_number')
        expiry_date = request.data.get('expiry_date')
        cvv = request.data.get('cvv')

        # Fetch the customer and validate
        try:
            customer = Customer.objects.get(id=customer_id)
            if not customer:
                return Response({"message": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"message": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the cake and validate
        try:
            cake = Cake.objects.get(id=cake_id)
            if not cake:
                return Response({"message": "Cake not found"}, status=status.HTTP_400_BAD_REQUEST)
            if not cake.available:
                return Response({"message": "Cake not available"}, status=status.HTTP_400_BAD_REQUEST)
        except Cake.DoesNotExist:
            return Response({"message": "Cake not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # fetching the cart 
        cart_item = Cart.objects.filter(customer=customer, cake=cake).first()
        if not cart_item:
            return Response({"message": "Cart item not found for the specified customer and cake"}, status=status.HTTP_404_NOT_FOUND)

        # Validate payment_method
        if payment_method not in ['debit_card' , 'credit_card' , 'cash']:
            return Response({"message": "Invalid payment method"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate card details
        if not self.validate_card(card_number, expiry_date, cvv):
            return Response({"message": "Invalid card details"}, status=status.HTTP_400_BAD_REQUEST)

        # Update order instance fields
        order_instance.payment_method = payment_method
        order_instance.payment_status = 'paid'
        order_instance.order_status = 'shipped'
        order_instance.order_date = timezone.now()
        order_instance.save()


        my_mail="sundramsharma12244@gmail.com"

        # sending confirmation mail
        subject = 'Congratulations! Your Order Has Been Placed'
        html_message = render_to_string('email.html', {
            'order_id': order_id,
            'customer_name': customer.first_name + ' ' + customer.last_name,
            'cake_name': cake.name,
        })
        plain_message = strip_tags(html_message)  # Remove HTML tags for plain text message
        from_email = 'itsundramsharma@gmail.com'  # Your Gmail email address
        to_email = [my_mail]  # Email address of the customer who placed the order

        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

        # deleting the cart
        cart_item.delete()

        return Response({"message": "Congratulations! Your order is successfully placed."},status=status.HTTP_200_OK)
    
    def schedule_mail(self,send_time, subject, message, recipient_list):
        delay = (send_time - now()).total_seconds()
        scheduler.enter(delay, 1, send_mail , argument=(subject, message, settings.EMAIL_HOST_USER, recipient_list))

    @action(detail=False, methods=['GET'], url_path='delivery-tracking/(?P<id>[^/]+)')
    def delivery_tracking(self,request,id):
        try:
            order_id=id
            order=Order.objects.get(id=id)
        except:
            return Response({"message": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            gmaps=googlemaps.Client(key="Your-API-Key")

            sweetspot_location="Gopal sweets,Kanpur, India"
            delivery_location=order.delivery_address
            
            distance_matrix=gmaps.distance_matrix(sweetspot_location,delivery_location)
            
            if distance_matrix['status']=='OK':
                distance = distance_matrix['rows'][0]['elements'][0]['distance']['text']
                duration=distance_matrix['rows'][0]['elements'][0]['duration']['text']

                print(duration)
                minutes = int(duration.split()[0])


                delivery_time=now() + timedelta(minutes=minutes)
                remainder_time=delivery_time-timedelta(minutes=5)
                print(duration)

                # First mail: Confirmation of delivery
                confirmation_subject = f'Confirmation of Delivery: Order {order_id}'
                confirmation_message = f'Your order (ID: {order_id}) is confirmed. It will be delivered to {order.delivery_address} in {duration}.'
                self.schedule_mail(now(), confirmation_subject, confirmation_message, [settings.EMAIL_HOST_USER])
                print(duration)

                # Second mail: 5 minutes remaining
                five_minutes_subject = f'5 Minutes Remaining: Order {order_id}'
                five_minutes_message = f'Your order (ID: {order_id}) is now 5 minutes away from your location.'
                self.schedule_mail(remainder_time, five_minutes_subject, five_minutes_message, [settings.EMAIL_HOST_USER])
                print(duration)
                
                # Third mail: Order at doorstep
                doorstep_subject = f'Order Delivered: Order {order_id}'
                doorstep_message = f'Your order (ID: {order_id}) has been delivered to your doorstep.'
                self.schedule_mail(delivery_time, doorstep_subject, doorstep_message, [settings.EMAIL_HOST_USER])
                print(duration)

                return Response({'order_id':id,'distance':distance,'duration':duration},status=status.HTTP_200_OK)
            else:
                return Response({"message": "API is not responding ."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

from rest_framework import permissions
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated , AllowAny

# Admin-exclusive ViewSets




class AdminCustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated ,IsAdminUser]



class AdminCakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer
    permission_classes = [IsAuthenticated ,IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]
        return [IsAdminUser()]
    
    


class AdminCakeCustomizationViewSet(viewsets.ModelViewSet):
    queryset = CakeCustomization.objects.all()
    serializer_class = CakeCustomizationSerializer
    permission_classes = [IsAuthenticated ,IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]
        return [IsAdminUser()]
    


class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated ,IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAdminUser()]
        return [IsAdminUser()]
    


class AdminStoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated ,IsAdminUser]



    def get_permissions(self):
        # Override to allow unrestricted access to 'store_has_cakes' action
        if self.action == 'store_has_cakes':
            return [permissions.AllowAny()]
        return super().get_permissions()


# Now user can fetch all the cakes for a particular store.

    @action(detail=True, methods=['get'], url_path='store-has-cakes')
    def store_has_cakes(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response({"message": "Store not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cakes = Cake.objects.filter(store=store)
        serializer = CakeSerializer(cakes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
