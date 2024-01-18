from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from partsapp import forms
from partsapp.forms import LoginUserForm, RegisterUserForm, OrderForm, CustomerForm
from partsapp.models import Product, Category, CarModel, ActiveContext, CartProduct, Customer
from partsapp.modules.services.mixins import CartMixin, DataMixin
from partsapp.modules.services.utils import recalc_cart


class PartsHome(DataMixin, ListView):
    template_name = 'partsapp/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_mixins_context()
        return context

    def get_queryset(self):
        return Product.objects.all()[:10]


class AboutView(DataMixin, TemplateView):
    template_name = 'partsapp/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_mixins_context()
        return context


class CatalogProducts(DataMixin, ListView):
    template_name = 'partsapp/catalog.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get("slug_cat"):
            ActiveContext.active_category = self.kwargs.get("slug_cat")
        if self.kwargs.get("slug_model"):
            ActiveContext.active_model = self.kwargs.get("slug_model")

        context |= self.get_mixins_context()

        return context

    def get_queryset(self):
        if self.kwargs['slug_model'] == CarModel.NAME_ALL_MODELS and self.kwargs['slug_cat'] \
                == Category.NAME_ALL_CATEGORIES:
            return Product.objects.all()[:10]
        elif self.kwargs['slug_model'] == CarModel.NAME_ALL_MODELS:
            return Product.objects.filter(category__slug=self.kwargs['slug_cat']).select_related("category")
        elif self.kwargs['slug_cat'] == Category.NAME_ALL_CATEGORIES:
            return Product.objects.filter(car_model__slug=self.kwargs['slug_model']).prefetch_related("car_model")

        return Product.objects.filter(category__slug=self.kwargs['slug_cat']).select_related("category"). \
            filter(car_model__slug=self.kwargs['slug_model']).prefetch_related("car_model")


class ProductDetail(DataMixin, DetailView):
    template_name = 'partsapp/product_detail.html'
    model = Product
    slug_url_kwarg = 'slug_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_mixins_context()
        return context


class SearchPageView(DataMixin, TemplateView):
    template_name = 'partsapp/search.html'

    def get(self, request, *args, **kwargs):
        form = forms.SearchForm(request.GET)

        if form.is_valid():

            query_number = form.clean_query().get('query_number')
            query_name = form.clean_query().get('query_name')

            context = {}
            context |= self.get_mixins_context()

            if query_number:
                object_list = Product.objects.filter(number=query_number)
            elif query_name and ActiveContext.active_model != CarModel.NAME_ALL_MODELS:
                object_list = Product.objects.filter(name__contains=query_name,
                                                     car_model__slug=ActiveContext.active_model).prefetch_related(
                    "car_model")
            elif query_name:
                object_list = Product.objects.filter(name__contains=query_name)

            text_page = ''
            if not object_list:
                text_page = "Ничего не найдено"

            paginator = Paginator(object_list, 8)
            page_number = request.GET.get('page', 1)
            paginator_lst = paginator.get_page(page_number)

            context |= {"query_number": query_number,
                        "query_name": query_name,
                        "object_list": paginator_lst,
                        "text_page": text_page}

            return render(request, self.template_name, context)

        return render(request,
                      self.template_name,
                      {"query_number": request.GET['query_number'],
                       "query_name": request.GET['query_name']})


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'partsapp/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_mixins_context()
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'partsapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_mixins_context()
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class CartView(CartMixin, DataMixin, View):

    def get(self, request, *args, **kwargs):
        context = {'cart': self.cart}
        context |= self.get_mixins_context()

        return render(request, 'partsapp/cart.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        url_redirect = reverse('cart')
        return HttpResponseRedirect(url_redirect)


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")

        url_redirect = reverse('cart')
        return HttpResponseRedirect(url_redirect)


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")

        url_redirect = reverse('cart')
        return HttpResponseRedirect(url_redirect)


class CheckoutView(CartMixin, DataMixin, View):

    def get(self, request, *args, **kwargs):
        context_inital = {"first_name": self.request.user.first_name,
                          "last_name": self.request.user.first_name}
        cust = Customer.objects.filter(user=self.request.user.id)[:1]
        if cust:
            current_customer = cust[0]
            context_inital |= {"phone": current_customer.phone,
                               "address": current_customer.address}
        form = OrderForm(request.POST or None, initial=context_inital)
        context = {
            'cart': self.cart,
            'form': form
        }
        context |= self.get_mixins_context()
        return render(request, 'partsapp/checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect(reverse('home'))
        return HttpResponseRedirect(reverse('checkout'))


class CustomerView(DataMixin, CreateView):
    form_class = CustomerForm
    template_name = 'partsapp/customer.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self, *args, **kwargs):
        result = super().get_form_kwargs(*args, **kwargs)
        cust = Customer.objects.filter(user=self.request.user.id)[:1]
        if cust:
            current_customer = cust[0]
            result |= {'initial': {'phone': current_customer.phone, 'address': current_customer.address}}
        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= self.get_mixins_context()
        return context

    def form_valid(self, form):
        customer = form.save(commit=False)
        cust = Customer.objects.filter(user=self.request.user.id)[:1]
        if cust:
            current_customer = cust[0]
            current_customer.phone = customer.phone
            current_customer.address = customer.address
        else:
            current_customer = customer
            current_customer.user = self.request.user

        current_customer.save()
        return redirect('home')
