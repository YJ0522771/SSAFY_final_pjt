from rest_framework import serializers
from .models import Movie, Genre
# from ..community.serializers import ReviewSerializer

# class MovieListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'


# class MovieSerializer(serializers.ModelSerializer):
#     review_set = ReviewSerializer(read_only=True, many=True)
#     review_count = serializers.IntegerField(source='review_set.count', read_only=True)
#     class Meta:
#         model = Movie
#         fields = '__all__'