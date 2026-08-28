from django.contrib import admin

from products.models import Category, Product , ProductVariants



# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
      model = Category
      list_display = [ "id","name" , "is_available"]



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
      model = Product
      list_display = [ "id","name" , "category" , "brand", "price" , "is_available" ]



@admin.register(ProductVariants)
class ProductVariant(admin.ModelAdmin):
      model = ProductVariants
      list_display = ["id" ,"product" , "size" , "color" ,"quantity" , "is_available"]


