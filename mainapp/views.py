from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
from datetime import date
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger
import stripe
from django.conf import settings
from django.http import JsonResponse


def index(request):
    # if request.user.is_authenticated:
    #     last_chat = Chat.objects.filter(
    #         Q(sender=request.user)).order_by('-created_at')[0]
    # else:
    #     last_chat = None
    not_found = ''
    if request.GET:
        query = request.GET.get('query')
        if query:
            services = Service.objects.filter(
                Q(category__name__icontains=query))
            if not services:
                not_found = 'По вашему запросу ничего не найдено'
            context = {
                'heading': 'Search results',
                'services': services,
                'categories': Category.objects.all(),
                'not_found': not_found,

            }
            return render(request, 'project__services.html', context)

    context = {
        'heading': 'Test page',
        # 'last_chat': last_chat,
        'categories': Category.objects.all(),
        'not_found': not_found,
    }
    return render(request, 'index.html', context)


def profile(request, id):
    user = CustomUser.objects.get(id=id)
    print(user)
    form = UserEditForm(instance=user)
    if request.POST:
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', id=request.user.id)
    context = {
        'heading': 'Profile page',
        'form': form,
    }
    if request.user == user:
        return render(request, 'userProf__editorial.html', context)
    else:
        return render(request, 'userProf__saw.html', context)


def login_user(request):
    if request.POST:
        # email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {'form': UserForm,
                       'error': 'Неверный логин или пароль'}
            return render(request, 'enter.html', context)
    context = {'form': UserForm}

    return render(request, 'enter.html', context)


def register(request):
    form = CustomUserCreationForm()
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and ('offer' in request.POST):
            user = form.save(commit=False)
            email = request.POST['email']
            already_exists = CustomUser.objects.filter(email=email).exists()
            if not already_exists:
                user.save()
                user = authenticate(
                    request, username=request.POST['username'], password=request.POST['password1'])
                login(request, user)
                return redirect('index')
            else:
                context = {
                    'form': form,
                    'email_error': 'Такой email уже зарегистрирован',
                }
                return render(request, 'registration.html', context)
        else:
            context = {
                'form': form,
                'offer_error': 'Подтвердите согласие с правилами',
            }
            return render(request, 'registration.html', context)
    context = {'form': form}
    return render(request, 'registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def project_page(request):
    orders = Order.objects.filter(status='pending')
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    if request.GET.get('query'):
        query = request.GET.get('query')
        orders = Order.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query))
    try:
        selected_categories = request.GET.getlist('category')
    except:
        pass
    if selected_categories:
        orders = Order.objects.filter(
            Q(category__name__in=selected_categories) & Q(status='pending'))
    catefories = Category.objects.all()
    context = {
        'orders': orders,
        'categories': catefories
    }
    return render(request, 'project__orders.html', context)


def project_detail(request, pk: int):
    order = Order.objects.get(pk=pk)
    order.views += 1
    order.save()
    chosen_date = order.deadline
    days_left = (chosen_date - date.today()).days
    owner_waiting_orders = Order.objects.filter(
        Q(owner=order.owner) & Q(status='pending'))
    owner_active_orders = Order.objects.filter(
        Q(owner=order.owner) & Q(status='completed'))
    unique_chat_key = uuid.uuid4()
    context = {
        'order': order,
        'days_left': days_left,
        'owner_waiting_orders': owner_waiting_orders,
        'owner_active_orders': owner_active_orders,
        'unique_chat_key': unique_chat_key
    }
    return render(request, 'targetedAdvertisingOne.html', context)


def services_page(request):
    services = Service.objects.all()
    paginator = Paginator(services, 10)
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        services = paginator.page(1)
    if request.GET.get('query'):
        query = request.GET.get('query')
        services = Service.objects.filter(
            Q(category__name__icontains=query) | Q(owner__username__icontains=query) | Q(
                owner__first_name__icontains=query) | Q(service_type__name__icontains=query))
    categories = Category.objects.all()
    context = {
        'services': services,
        'categories': categories
    }
    return render(request, 'project__services.html', context)


def chat_page(request, id):
    user = request.user
    order = Order.objects.get(
        Q(id=id))
    chat = None
    sender_chats = Chat.objects.filter(sender=user)
    send_to_chats = Chat.objects.filter(send_to=user)
    try:
        chat = Chat.objects.get(Q(send_to=order.owner) & Q(sender=user))
    except:
        pass

    if chat is None:
        try:
            chat = Chat.objects.get(Q(send_to=user) & Q(sender=order.owner))
        except:
            pass

    if chat is None and (order.owner != user):
        chat = Chat.objects.create(
            sender=user,
            send_to=order.owner
        )
        chat.save()

    try:
        message = Message.objects.filter(chat=chat)
    except:
        message = None

    if request.POST:
        new_message = request.POST.get('message')
        new_message = Message.objects.create(
            chat=chat,
            sender=user,
            text=new_message
        )
        new_message.save()
        return redirect('chat', id=id)

    context = {
        'chat': chat,
        'messages': message,
        'sender_chats': sender_chats,
        'send_to_chats': send_to_chats
    }
    return render(request, 'messages.html', context)


def chat_with_freelancer(request, username):
    user = request.user
    freelancer = CustomUser.objects.get(username=username)
    chat = None
    sender_chats = Chat.objects.filter(sender=user)
    send_to_chats = Chat.objects.filter(send_to=user)
    try:
        chat = Chat.objects.get(Q(send_to=freelancer) & Q(sender=user))
    except:
        pass

    if chat is None:
        try:
            chat = Chat.objects.get(Q(send_to=user) & Q(sender=freelancer))
        except:
            pass

    if chat is None:
        chat = Chat.objects.create(
            sender=user,
            send_to=freelancer
        )
        chat.save()

    try:
        message = Message.objects.filter(chat=chat)
    except:
        message = None

    if request.POST:
        new_message = request.POST.get('message')
        new_message = Message.objects.create(
            chat=chat,
            sender=user,
            text=new_message
        )
        new_message.save()
        return redirect('chat-with-freelancer', username=username)

    context = {
        'chat': chat,
        'messages': message,
        'sender_chats': sender_chats,
        'send_to_chats': send_to_chats
    }
    return render(request, 'messages.html', context)


def freelancers_page(request):
    freelancers = CustomUser.objects.filter(user_type_id=1)
    categories = Category.objects.all()
    paginator = Paginator(freelancers, 10)
    page = request.GET.get('page')

    try:
        freelancers = paginator.page(page)
    except PageNotAnInteger:
        freelancers = paginator.page(1)
    not_found = ''
    if request.GET.get('query'):
        query = request.GET.get('query').capitalize()
        freelancers_found = CustomUser.objects.filter(
            Q(user_type_id=1) & Q(first_name__icontains=query)
        )

        if not freelancers_found:
            freelancers = None
            not_found = 'Такого пользователя не существует'
    context = {
        'freelancers': freelancers,
        'categories': categories,
        'not_found': not_found
    }
    return render(request, 'project__specialists.html', context)


def my_orders_page(request, status):
    user = request.user
    orders = Order.objects.filter(Q(owner=user) & Q(status=status))
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    print(user.user_type_id)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    if request.GET.get('query'):
        query = request.GET.get('query')
        orders = Order.objects.filter(
            Q(owner=user) & Q(status=status) & Q(title__icontains=query))
    page = status
    context = {
        'orders': orders,
        'page': page
    }
    return render(request, 'myProject.html', context)


def my_orders_page_freelancer(request, status):
    user = request.user
    orders = Order.objects.filter(Q(freelancer=user) & Q(status=status))
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    if request.GET.get('query'):
        query = request.GET.get('query')
        orders = Order.objects.filter(
            Q(owner=user) & Q(status=status) & Q(title__icontains=query))
    page = status
    context = {
        'orders': orders,
        'page': page
    }
    return render(request, 'myProjectFreelancer.html', context)


def my_order_active_detail(request, order_id):
    user = request.user
    order = Order.objects.get(id=order_id)
    try:
        feedback = OrderFeedback.objects.get(Q(order=order) & Q(sender=user))
    except:
        feedback = None
    if request.POST:
        new_feedback = request.POST.get('feedback')
        new_feedback = OrderFeedback.objects.create(
            order=order,
            sender=user,
            feedback=new_feedback
        )
        new_feedback.save()
        return redirect('my-orders-freelancer-detail', order_id=order_id)
    context = {
        'order': order,
        'feedback': feedback
    }
    return render(request, 'targetedAdvertisingOneActive.html', context)


def my_order_completed(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'completed'
    order.save()
    return redirect('my-orders-freelancer', 'pending')


def my_order_canceled(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'cancelled'
    order.save()
    return redirect('my-orders-freelancer', 'pending')


def create_order_page(request):
    form = OrderForm()
    user_id = request.user.id
    if request.POST:
        form = OrderForm(request.POST)
        print(request.POST)

        if form.is_valid():
            form.save()
            return redirect('my-orders', 'pending')
    context = {
        'form': form,
        'user_id': user_id
    }
    return render(request, 'add__t__task.html', context)


def error_page(request):
    return render(request, 'error__page.html')


def wallet_page(request):
    user = request.user
    try:
        wallet = Wallet.objects.get(owner=user)
        orders = Order.objects.filter(owner=user)
    except:
        wallet = Wallet.objects.create(
            owner=user,
            balance=0
        )
        orders = None
    if request.POST:
        payment = Payment.objects.create(
            owner=user,
            amount=100
        )
    context = {
        'user': user,
        'wallet': wallet,
        'orders': orders
    }
    return render(request, 'onlineWallet.html', context)


def payment_first_step(request):
    user = request.user
    wallet = Wallet.objects.get(owner=user)
    payment = Payment.objects.create(
        owner=user,
        amount=100
    )
    payment.save()
    if request.POST:
        amount = request.POST.get('amount')
        # wallet.balance = new_balance
        # wallet.save()
        return redirect('payment-second-step', payment_id=payment.id)
    context = {
        'user': user,
        'wallet': wallet
    }
    return render(request, 'walletReplenishment.html', context)


def payment_second_step(request, payment_id):
    user = request.user
    wallet = Wallet.objects.get(owner=user)
    payment = Payment.objects.get(pk=payment_id)
    print(payment)
    if request.POST:
        amount = request.POST.get('amount')
        # wallet.balance = new_balance
        # wallet.save()
        return redirect('payment-third-step')
    context = {
        'user': user,
        'wallet': wallet,
        'payment': payment
    }
    return render(request, 'walletReplenishmentSecond.html', context)


def get_item_by_id(request, pk):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    current_item = CustomUser.objects.get(id=pk)
    get_product_id_stripe = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': Пополнение,
                },
                'unit_amount': Стоимость,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/',
        cancel_url='http://localhost:8000/',
    )
    return JsonResponse(get_product_id_stripe)
