from django.urls import path


from partsapp.views import PartsHome, CatalogProducts, ProductDetail, SearchPageView, LoginUser, logout_user, \
    RegisterUser, CartView, AddToCartView, ChangeQTYView, DeleteFromCartView, CheckoutView, MakeOrderView, AboutView, \
    CustomerView

urlpatterns = [
    path('', PartsHome.as_view(), name='home'),
    path('index/', PartsHome.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('catalog/<slug:slug_cat>/<slug:slug_model>', CatalogProducts.as_view(), name='catalog'),
    path('product-detail/<slug:slug_product>/', ProductDetail.as_view(), name='product_detail'),
    path('search/', SearchPageView.as_view(), name='search_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('customer/<int:user_id>/', CustomerView.as_view(), name='customer'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('change-qty/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order')
]
