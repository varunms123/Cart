from django.shortcuts import render,redirect
from rest_framework import status
from .models import *
from django.http import *
from rest_framework.response import Response
import base64
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.db.models import Sum
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

# Create your views here.

def index(request):
    category = Category.objects.get(category="Featured Products")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item': cart_items, 'cart_total': cart_total,'product':product}
    return render(request, 'index.html', context)

def remove(request,id):
    try:
        cart = CartItems.objects.get(id=id)
        cart.delete()
    except CartItems.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def men_product(request):
    category = Category.objects.get(category="Men's Fashion")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item': cart_items, 'cart_total': cart_total,'product':product}
    return render(request, 'men.html', context)


def women_product(request):
    category = Category.objects.get(category="Women's Fashion")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item': cart_items, 'cart_total': cart_total,'product':product}
    return render(request,'women.html',context)

def mobiles(request):
    category = Category.objects.get(category="Mobiles")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item': cart_items, 'cart_total': cart_total,'product':product}
    return render(request,'mobiles.html',context)

def laptops(request):
    category = Category.objects.get(category="Laptops")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item':cart_items,'cart_total':cart_total,'product':product}
    return render(request,'laptops.html',context)

def kitchen(request):
    category = Category.objects.get(category="Kitchen")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item':cart_items,'cart_total':cart_total,'product':product}
    return render(request,'kitchen.html',context)

def headphones(request):
    category = Category.objects.get(category="Headphones")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item':cart_items,'cart_total':cart_total,'product':product}
    return render(request,'headphones.html',context)

def books(request):
    category = Category.objects.get(category="Books")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item':cart_items,'cart_total':cart_total,'product':product}
    return render(request,'books.html',context)

def shoes(request):
    category = Category.objects.get(category="Shoes")
    product = Product.objects.filter(category=category)
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item':cart_items,'cart_total':cart_total,'product':product}
    return render(request,'shoes.html',context)

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('wpforms[fields][0]')
        subject = request.POST.get('wpforms[fields][5]')
        email = request.POST.get('wpforms[fields][4]')
        message = request.POST.get('wpforms[fields][2]')

        contact_form = ContactForm(name=name, subject=subject, email=email, message=message)
        contact_form.save()

        return redirect('/')
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item':cart_items,'cart_total':cart_total}
    return render(request, 'contact.html',context)

@csrf_exempt
def add_product(request,id):
    try:
        product = Product.objects.get(id=id)
        cart_items = CartItems.objects.all()
        cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
        context = {'cart_item': cart_items, 'cart_total': cart_total,'product':product}
        if request.GET.get('product'):
            price = product.get_product_price(price)
            context['updated_price'] = price
        return render(request,'product.html',context)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

@csrf_exempt
def cart(request, id):
    if request.method == "POST":
        product = None
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return render(request, 'product_not_found.html')

        quantity = int(request.POST.get('quantity'))
        price = product.price
        total_price = product.price * quantity

        cart_item = CartItems(product=product,price=price, quantity=quantity, total_price=total_price)
        cart_item.save()

        return redirect('login')

    return HttpResponse("Invalid request method.")

@csrf_exempt 
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = MyUser.objects.get(email=email,password=password)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        if user:
            return redirect("view")
        
    return render(request, 'login.html')
    
def register(request):
    if request.method == "POST":
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')  
            password = request.POST.get('password')

            if MyUser.objects.filter(email=email).exists():
                messages.error(request,"Email already exists")
                return redirect("register")
            
            if email is None or not email.endswith('@gmail.com'):
                messages.error(request,"Email must end with only @gmail.com")
                return redirect("register")
            
            if email and password is None:
                messages.error(request,"email and password cannot be empty")
                return redirect("register")
            else:
                user = MyUser.objects.create(name=name,phone=phone,email=email,password=password)
                user.save()
                return redirect("login")

    return render(request, 'register.html')

def view(request):
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_item': cart_items, 'cart_total': cart_total}
    return render(request, 'cart.html', context)

@csrf_exempt
def checkout(request):
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    context = {'cart_items': cart_items, 'cart_total': cart_total}
    return render(request, 'checkout.html', context)


def get_product(request,id):
    try:
        product = Product.objects.get(id=id)
        context = {'product':product}

        if request.GET.get('product'):
            price = product.get_product_price(price)
            context['price'] = price

        return render(request,'product.html',context=context)
    except Product.DoesNotExist:
        raise Http404("Product Does not exist")

from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def category(request):
    if request.method == "POST":
        category = request.POST.get('category')
        try:
            existing_category = Category.objects.get(category=category)
            return Response({'error': 'Category already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ObjectDoesNotExist:
            new_category = Category.objects.create(category=category)
            new_category.save()
            return Response({'message': 'Category added successfully'})

@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def post_product(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.POST.get('image')
        size = request.POST.get('size')

        try:
            cat = Category.objects.get(category=category)
        except Category.DoesNotExist:
            return HttpResponse({'error': 'Invalid Category'}, status=status.HTTP_400_BAD_REQUEST)

        if Product.objects.filter(product_name=product_name).exists():
            return Response({'error': 'Product with same name already exists'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            converted_image = convertBase64(image, product_name, category)
            product = Product.objects.create(product_name=product_name,category=cat,price=price,description=description,image=converted_image,size=size)
            return Response({'message':'Product Added Successfully'})
    return HttpResponse("Invalid request method")


# def post(self,request):
#         # CheckAccess(request)
#         data = request.data
#         vehicle_type_name=data.get('vehicle_type_name')
#         capacity=data.get('capacity')
#         size=data.get('size')
#         details=data.get('details')
#         per_km_price = data.get('per_km_price')
#         min_charge = data.get('min_charge')
#         max_time_min = data.get('max_time_min')
#         badge = data.get('badge')
#         per_min_price=data.get('per_min_price')
#         vehicle_type_image=data.get('vehicle_type_image')
#         vehicle_description=data.get('vehicle_description')
#             # return Response({i})
#         # converted_vehicle_type_image= vehicle_type_sub_images
#         # vehicle_type_sub_images=converted_vehicle_type_image
#         # vehicle_type_sub_images={}
#         # converted_vehicle_type_sub_images=convertBase64(vehicle_type_image, 'vehicle_type_sub_images', size, "vehicle_type_image")
#         selected_page_no = 1
#         page_number = request.GET.get('page')

#         if page_number:
#             selected_page_no = int(page_number)


#         sub_image_list  = []
     
#         for i in data.get('vehicle_type_sub_images'):
#             print(i,'ii')
#             image_name = 'image'+str(random.randint(0,1000))
#             sub_image_data = convertBase64(i['image'], image_name, size, "vehicle_type_image")
#             sub_image_dic = {
#                 'image':sub_image_data
#             }
#             sub_image_list.append(sub_image_dic)

#         vehicle_type_discription_list=[]
#         descriptions=vehicle_description
#         vehicle_description_dict={
#             'description':descriptions
#         }
#         #


# class Delete_vehicle_imageApi(APIView):
#     def delete(self, request, vehicle_type_id):
#         img_index_id = request.query_params.get('img_index_id')  
#         des_index_id = request.query_params.get('des_index_id')    
#         if(img_index_id):    
#             val_obj=VehicleTypes.objects.get(id=vehicle_type_id)
#             img_list=val_obj.vehicle_type_sub_images
#             removed_value = img_list.pop(int(img_index_id))
#             update_vehicle_type_sub_img= VehicleTypes.objects.filter(id=vehicle_type_id).update(vehicle_type_sub_images=img_list)      
#             return Response({'data':'image deleted sucessfully!!!'})
#         else:
#             val_obj=VehicleTypes.objects.get(id=vehicle_type_id)
#             des_list=val_obj.vehicle_description
#             print('ggggggg=====>>>>',des_list)
#             removed_value = des_list[0]['description'].pop(int(des_index_id))
#             print('fgffffffffffffff=====>>',removed_value)
#             print('ggggg',des_list[0]['description'])
#             update_vehicle_type_sub_img= VehicleTypes.objects.filter(id=vehicle_type_id).update(vehicle_description=des_list)      
#             return Response({'data':'description deleted sucessfully!!!'})

def convertBase64(image,product_name,category):
    if image is None:
        return None

    split_base_url_data = image.split(';base64,')[1]
    img = base64.b64decode(split_base_url_data)
    category_path = os.path.join("media", category)
    os.makedirs(category_path, exist_ok=True)
    filename = os.path.join(category_path, "images", f"{product_name}.png")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename,'wb') as f:
        f.write(img)

    return os.path.join(category,'images',str(product_name) + '.png')

def place_order(request):
    try:
        if request.method == 'POST':
            full_name=request.POST.get('full_name')
            country = request.POST.get('country')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            selected_payment_method = request.POST.get('payment_method')
            
            if not (full_name and country and address and city and state and pincode and phone and email):
                messages.warning(request, "Please fill in all the required details.")
                return redirect('checkout')
            
            order = Orders(full_name=full_name, country=country, address=address, city=city, state=state,
                           pincode=pincode, phone=phone, email=email)
        
            cart_items = CartItems.objects.all()
            cart_total = cart_items.aggregate(total=Sum('total_price'))['total']

            if cart_items.exists():
                order.save()

            messages.success(request, "Order has been placed successfully.")
            return redirect('order_received',payment_method=selected_payment_method)
    except Orders.DoesNotExist:
        raise Http404("Please fill in the details")
    return render(request,'checkout.html')

def order_received(request,payment_method):
    payment_methods = {
        'bacs': 'Direct Bank Transfer',
        'cheque': 'Cheque Payments',
        'cod': 'Cash on Delivery',
        'paypal': 'PayPal'
    }
    cart_items = CartItems.objects.all()
    cart_total = cart_items.aggregate(total=Sum('total_price'))['total']
    payment_method_name = payment_methods.get(payment_method, '')
    context = {'cart_items': cart_items, 'cart_total': cart_total,'payment_method': payment_method_name}
    return render(request, 'order_received.html',context)   

@csrf_exempt
def review(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        product_name = request.POST.get('product_name')

        if name and email and review and rating and product_name:
            review_obj = Review.objects.create(name=name, email=email, reviews=review, rating=rating,product_name=product_name)
            review_obj.save()
            return redirect("index")
        else:
            return HttpResponse("All fields are required.")

    return HttpResponse("Invalid request")