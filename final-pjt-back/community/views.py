import re
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.apps import apps
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import requires_csrf_token

from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
# from ..movies.models import Movie 
import datetime

'''
def get_time(time):
    now = datetime.datetime.now()
    
    year = time[:4]
    month = time[5:7]
    day = time[8:10]
    hour = time[11:13]
    minute = time[14:16]
    second = time[17:19]
    # print(now.day)
    # print(year, month, day, hour, minute, second)
    in_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    # print(now - in_time)

    if now - in_time >= datetime.timedelta(days=30):
        return '{}년{}월{}일 {}시{}분'.format(year, month, day, hour, minute)
    elif now - in_time >= datetime.timedelta(days=1):
        return '{}일 전'.format((now - in_time).days)
    elif now - in_time >= datetime.timedelta(hours=1):
        return '{}시간 전'.format((now - in_time).seconds // 3600)
    elif now - in_time >= datetime.timedelta(minutes=1):
        return '{}분 전'.format((now - in_time).seconds // 60)
    else:
        return '방금 전'
'''

@api_view(['GET'])
def review_list(request, movie_id):
    Movie = apps.get_model('movies', 'Movie')
    movie = get_object_or_404(Movie , pk = movie_id)
    reviews = movie.reviews.all().order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    reviews = serializer.data

    res = []
    for review in reviews:
        user = get_user_model().objects.get(id=review['user'])
        temp = {
            'id': review['id'],
            'title': review['title'],
            'content': review['content'],
            'vote': review['vote'],
            'username': user.username,
            'user_id': review['user'],
            'movie_id': review['movie'],
            'created_at': review['created_at'],
            'updated_at' : review['updated_at']
        }
        res.append(temp)
        
    return Response(res)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_create(request, movie_id):
    Movie = apps.get_model('movies', 'Movie')
    movie = get_object_or_404(Movie , pk = movie_id)
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        movie.vote_count += 1
        movie.vote_average = round(
            ((movie.vote_average * (movie.vote_count - 1)) + float(request.data['vote']) ) 
            / movie.vote_count, 1)
        movie.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    # print(get_object_or_404(Review, pk=review_id))
    # serializer = ReviewSerializer(review)
    user = get_user_model().objects.get(id=review.user.id)
    res = {
            'id': review.id,
            'title': review.title,
            'content': review.content,
            'vote': review.vote,
            'username': user.username,
            'user_id': review.user.id,
            'movie_id': review.movie.id,
            'created_at': review.created_at, 
            'updated_at' : review.updated_at
        }
    return Response(res)



@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_put_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    Movie = apps.get_model('movies', 'Movie')
    movie = get_object_or_404(Movie , pk = request.data['movie_id'])
    if request.user == review.user :
        if request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            c_vote = review.vote
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                movie.vote_average = round(
                    ((movie.vote_average * (movie.vote_count)) + 
                    float(request.data['vote']) - float(c_vote) ) 
                    / movie.vote_count, 1)
                movie.save()
                return Response(serializer.data)
        
        elif request.method == 'DELETE':
            movie.vote_count -= 1
            if (movie.vote_count) :
                movie.vote_average = round(
                    ((movie.vote_average * (movie.vote_count + 1)) - 
                    float(request.data['vote'])) 
                    / movie.vote_count, 1)
            else:
                movie.vote_average = 0
            movie.save()
            review.delete()
            return Response({'id': review_id}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def comment_list(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comments = review.comments.all().order_by('-created_at')

    res = []
    for comment in comments:
        user = get_user_model().objects.get(id=comment.user.id)
        temp = {
            'id': comment.id,
            'content': comment.content,
            'username': user.username,
            'user_id': comment.user.id,
            'review_id': comment.review.id,
            'created_at': comment.created_at,
            'updated_at' : comment.updated_at
        }
        res.append(temp)

    # serializer = CommentSerializer(comments, many=True)
    return Response(res)


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user:
        comment.delete()
        return Response({'id': comment_id}, status=status.HTTP_204_NO_CONTENT)

