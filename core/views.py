from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View, ListView, DetailView

from .models import Item, OrderItem, Order
from .forms import CheckoutForms


class ProductListView(ListView):
    model = Item
    template_name = 'index.html'
    paginate_by = 8
    context_object_name = 'items'


class DetailsView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'products'


class Cart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have an active cart")
            return redirect('/')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:cart")


@login_required
def remove_signle_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity updated")
            return redirect('core:cart')
        else:
            messages.warning(request, "this item is not in your cart")
            return redirect('core:index')
    else:
        messages.info(request, "you don't have an active order")
        return redirect('/')


@login_required
def remove_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "this item removed from your cart")
            return redirect('/')
        else:
            messages.info(request, "this item not in your cart")
            return redirect('/')

    else:
        messages.info(request, "you dont have an active card")
        return redirect('/')


@login_required
def clearcart(request):
    cart = OrderItem.objects.filter(
        user=request.user,
        ordered=False
    )
    if cart.exists():
        cart.delete()
    return redirect('/')


class Checkout(View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForms
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)
