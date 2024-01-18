from django.views import View

from partsapp.models import Category, CarMark, CarModel, ActiveContext, Customer, Cart


class CategoryMixin:

    def get_all_categories(self):
        categories = Category.objects.all()
        active_category_obj = None
        if ActiveContext.active_category != Category.NAME_ALL_CATEGORIES:
            active_category_obj = Category.objects.filter(slug=ActiveContext.active_category)[0]
        return {'categories': categories
            , 'name_all_categories': Category.NAME_ALL_CATEGORIES
            , 'active_category': ActiveContext.active_category
            , 'active_category_obj': active_category_obj
                }


class ModelMixin:

    def get_all_mark_and_model(self):
        result = []
        marks = CarMark.objects.all()
        for el in marks:
            models = CarModel.objects.filter(car_mark=el.id)
            result.append({"name_mark": el.name, "models": models})
        active_model_obj = None
        if ActiveContext.active_model != CarModel.NAME_ALL_MODELS:
            active_model_obj = CarModel.objects.filter(slug=ActiveContext.active_model)[0]
        return {"marks_models": result
            , "name_all_models": CarModel.NAME_ALL_MODELS
            , 'active_model': ActiveContext.active_model
            , 'active_model_obj': active_model_obj
                }


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)

        ActiveContext.active_cart = cart
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)


class DataMixin(CategoryMixin, ModelMixin):

    def get_mixins_context(self):
        result = {}
        result |= self.get_all_categories()
        result |= self.get_all_mark_and_model()
        if ActiveContext.active_cart:
            result |= {'cart': ActiveContext.active_cart}
        return result
