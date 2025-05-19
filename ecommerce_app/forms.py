from ecommerce_app.models import Product, Review
from django.forms import ModelForm

class ProductForm(ModelForm):
  class Meta:
    model = Product
    fields = '__all__'

  def clean_product(self):
    name = self.clean_product['name']
    if Product.objects.filter(name = name).exists():
      raise ModelForm.validate_unique("This product already exists.")
    return name


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']