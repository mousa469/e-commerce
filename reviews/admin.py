from django.contrib import admin

from reviews.models import Review


# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
        model = Review
        list_display = ["id" , "review" , "rate" ,"product" , "product_id"]