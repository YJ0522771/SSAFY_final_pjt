from django.shortcuts import render, get_list_or_404, get_object_or_404

from .models import Movie, Genre
# from .serializers import MovieListSerializer, MovieSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import requests
import random


def data_encode(str):
    return str.replace('\u200b', ' ').replace('\u2013', ' ').replace('\xa0', ' ').strip()

# TMDB의 데이터를 DB에 추가하는 함수
def add_tmdb_data(request):
    GENRE_URL = 'https://api.themoviedb.org/3/genre/movie/list?api_key=89f79ed539b9acac12d99fad3d2ef1f8&language=ko-KR'
    genres = requests.get(GENRE_URL).json()
    genres = genres.get('genres')

    for genre in genres:
        if Genre.objects.filter(tmdb_id = genre.get('id')).exists():
            continue
        res = Genre.objects.create(
            tmdb_id = genre.get('id'),
            name = data_encode(genre.get('name'))
        )

    MOVIE_URL = 'https://api.themoviedb.org/3/movie/popular?api_key=89f79ed539b9acac12d99fad3d2ef1f8&language=ko-KR&region=KR&page='
    imgPath = 'https://image.tmdb.org/t/p/w500'

    for i in range(1, 51):
        movies = requests.get(MOVIE_URL + str(i)).json()
        movies = movies.get('results')

        for movie in movies:
            # 실수로 여러 번 실행하여도 같은 영화 정보가 중복되지 않도록
            if Movie.objects.filter(tmdb_id = movie.get('id')).exists():
                continue

            if movie.get('overview'):
                overview = data_encode(movie.get('overview'))
            else:
                overview = '줄거리 정보 없음.'

            res = Movie.objects.create(
                tmdb_id = movie.get('id'),
                title = data_encode(movie.get('title')),
                overview = overview,
                poster_path = imgPath + movie.get('poster_path'),
                release_date = movie.get('release_date'),
                vote_average = movie.get('vote_average'),
                vote_count = movie.get('vote_count')
            )
            print(res.title)

            for j in movie.get('genre_ids'):
                g = Genre.objects.get(tmdb_id = j)
                res.genres.add(g)

    PLAY_URL = 'https://api.themoviedb.org/3/movie/now_playing?api_key=89f79ed539b9acac12d99fad3d2ef1f8&language=ko-KR&region=KR&page='

    for i in range(1, 5):
        movies = requests.get(PLAY_URL + str(i)).json()
        movies = movies.get('results')

        for movie in movies:
            if Movie.objects.filter(tmdb_id = movie.get('id')).exists():
                temp = get_object_or_404(Movie, tmdb_id = movie.get('id'))
                temp.playing = True
                temp.save()

    return Response({'result': 'Success'})



# 랜덤으로 30개의 영화 정보
@api_view(['GET'])
def movie_random_list(request):
    SAMPLE_NUM = 35
    all_movies = get_list_or_404(Movie)
    
    l = len(all_movies)
    random_list = random.sample(list(range(l)), SAMPLE_NUM)

    movies = []
    for r in random_list:
        data = {
            'id':  all_movies[r].pk,
            'title': all_movies[r].title,
            'overview': all_movies[r].overview,
            'poster_path': all_movies[r].poster_path,
            'release_date': all_movies[r].release_date,
            'vote_average': all_movies[r].vote_average,
            'genres': []
        }
        for g in  all_movies[r].genres.all():
            data['genres'].append(g.name)
        movies.append(data)

    # serializer = MovieListSerializer(movies, many=True)
    return Response(movies)


@api_view(['GET'])
def movie_playing_list(request):
    movies = Movie.objects.filter(playing=True).order_by('-vote_average')
    
    res = []
    for movie in movies:
        data = {
            'id':  movie.pk,
            'title': movie.title,
            'overview': movie.overview,
            'poster_path': movie.poster_path,
            'release_date': movie.release_date,
            'vote_average': movie.vote_average,
            'genres': []
        }
        for g in  movie.genres.all():
            data['genres'].append(g.name)
        res.append(data)

    return Response(res)


@api_view(['GET'])
def movie_genre_list(request):
    genres = get_list_or_404(Genre)

    res = {}
    for genre in genres:
        res[genre.name] = []
        movies = Movie.objects.filter(genres=genre)

        for movie in movies:
            data = {
                'id':  movie.pk,
                'title': movie.title,
                'poster_path': movie.poster_path,
                'vote_average': movie.vote_average,
                'genres': []
            }
            for g in movie.genres.all():
                data['genres'].append(g.name)
            res[genre.name].append(data)

        SAMPLE_NUM = 7

        if len(res[genre.name]) > SAMPLE_NUM:
            random_list = random.sample(list(range(len(res[genre.name]))), SAMPLE_NUM)
            new = []
            for r in random_list:
                new.append(res[genre.name][r])
            res[genre.name] = list(new)
        
    # print(res)

    return Response(res)


@api_view(['GET'])
def movie_all_list(request):
    movies = Movie.objects.all()
    
    res = []
    for movie in movies:
        data = {
            'id':  movie.pk,
            'title': movie.title,
        }
        res.append(data)

    return Response(res)


@api_view(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    data = {
        'id': movie.pk,
        'title': movie.title,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'release_date': movie.release_date,
        'vote_average': movie.vote_average,
        'genres': []
    }
    for g in  movie.genres.all():
        data['genres'].append(g.name)

    return Response(data)


@api_view(['GET'])
# jwt 확인
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_recommend(request):
    genres = get_list_or_404(Genre)
    score = {}
    for genre in genres:
        score[genre.id] = 0
    
    user = request.user
    reviews = user.review_set.all()
    user_movies = []

    if len(reviews) == 0:
        return Response({'exists': False})

    for review in reviews:
        movie = get_object_or_404(Movie, pk = review.movie.id)
        user_movies.append(movie)
        genres = get_list_or_404(Genre, genre_movies = movie)
        for genre in genres:
            score[genre.id] += review.vote

    best = sorted(score.items(), key=lambda x:x[1], reverse=True)[:3]

    for i in range(3):
        if best[i][1] == 0:
            best = best[:i]
            break
    genre_ids = []
    for b in best:
        genre_ids.append(b)

    best_genres = []
    for id in genre_ids:
        best_genres.append(get_object_or_404(Genre, id=id[0]).name)

    temp_movies = []
    for gid in genre_ids:
        movies = get_list_or_404(Movie, genres = gid[0])
        temp_movies.append(movies)
    # print(len(temp_movies))
    
    score = {}
    # for i in range(1, len(Movie.objects.all().count())):
    #     score[i] = 0
    for i in range(len(temp_movies)):
        for temp in temp_movies[i]:
            if score.get(temp.id):
                score[temp.id] += 10 ** i 
            else:
                score[temp.id] = 10 ** i 

    res123 = []
    res12 = []
    res13 = []
    res23 = []
    for s in score.keys():
        if score[s] < 11:
            continue
        m = get_object_or_404(Movie, id=s)
        if m in user_movies:
            continue
        data = {
            'id':  m.pk,
            'title': m.title,
            'poster_path': m.poster_path,
            'vote_average': m.vote_average,
            'genres': []
        }
        for g in  m.genres.all():
            data['genres'].append(g.name)

        if score[s] == 111:
            res123.append(data)
        elif score[s] == 11:
            res12.append(data)
        elif score[s] == 101:
            res13.append(data)
        elif score[s] == 110:
            res23.append(data)

    print(len(res123))
    print(len(res12))
    print(len(res13))
    print(len(res23))

    SAMPLE_NUM = 14

    if len(res123) > SAMPLE_NUM:
        random_list = random.sample(list(range(len(res123))), SAMPLE_NUM)
        new = []
        for r in random_list:
            new.append(res123[r])
        res123 = list(new)
    if len(res12) > SAMPLE_NUM:
        random_list = random.sample(list(range(len(res12))), SAMPLE_NUM)
        new = []
        for r in random_list:
            new.append(res12[r])
        res12 = list(new)
    if len(res13) > SAMPLE_NUM:
        random_list = random.sample(list(range(len(res13))), SAMPLE_NUM)
        new = []
        for r in random_list:
            new.append(res13[r])
        res13 = list(new)
    if len(res23) > SAMPLE_NUM:
        random_list = random.sample(list(range(len(res23))), SAMPLE_NUM)
        new = []
        for r in random_list:
            new.append(res23[r])
        res23 = list(new)

    context = {
        'best_genres': best_genres,
        'recommend123': res123,
        'recommend12': res12,
        'recommend13': res13,
        'recommend23': res23,
        'exists': True
    }

    print(context)

    # print(len(res))
    # print(user_movies)
    return Response(context)



