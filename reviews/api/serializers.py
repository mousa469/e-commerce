from rest_framework import serializers

from reviews.models import Review



class ReviewSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    class Meta:
        model = Review
        fields = ["id" , "review" ,"rate","product" , "user" , "first_name" , "last_name" , "created_at", "updated_at"]





class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review" , "rate"]

