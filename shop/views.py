import stripe

from django.http import JsonResponse
from django.shortcuts import render, redirect

from TaskWithSprite.settings import STRIPE_SECRET_API_KEY, STRIPE_PUBLIC_API_KEY
from shop.models import Item

stripe.api_key = STRIPE_SECRET_API_KEY


def index(request):
    items = Item.objects.all()
    return render(request, 'shop/index.html', context={"items": items})


def show_item(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    if item:
        context = {"item": item, "public_api": STRIPE_PUBLIC_API_KEY}
        return render(request, 'shop/item.html', context=context)
    return redirect('index')


def get_session_id(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    if item:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/'),
            cancel_url=request.build_absolute_uri('/'),
        )

        return JsonResponse({'session_id': session.id})

    redirect('index')
