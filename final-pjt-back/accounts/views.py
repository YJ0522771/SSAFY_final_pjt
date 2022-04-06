from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.apps import apps
from django.shortcuts import get_object_or_404, get_list_or_404

@api_view(['POST'])
def signup(request):
	#1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	#1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	#2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	#3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
    # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다.
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_profile(request, username):
    user = get_user_model().objects.get(username=username)
    reviews = user.review_set.all().order_by('-created_at')

    user_movies = []
    user_genres = {}
    user_review_ids = []
    for review in reviews:
        # movie = get_object_or_404(Movie_model, id=re)
        data = {
            'id':  review.movie.pk,
            'title': review.movie.title,
            'poster_path': review.movie.poster_path,
            'vote_average': review.movie.vote_average,
            'review_id': review.id,
            'review_vote': review.vote,
            'review_title': review.title,
            'review_created':review.created_at,
            'genres': []
        }
        for g in review.movie.genres.all():
            data['genres'].append(g.name)
            if user_genres.get(g.name):
                user_genres[g.name] += review.vote
            else:
                user_genres[g.name] = review.vote

        if data not in user_movies:
            user_movies.append(data)
            # user_review_ids.append(review.id)

    best = sorted(user_genres.items(), key=lambda x:x[1], reverse=True)
    user_genres = {}
    g_sum = 0
    temp = 0
    for b in best:
        if b[1] == 0:
            break
        if len(user_genres) < 4:
            user_genres[b[0]] = b[1]
        g_sum += b[1]

    for g in user_genres.keys():
        user_genres[g] *= 100
        user_genres[g] = round(user_genres[g] / g_sum)
        temp += user_genres[g]

    if temp < 100 and len(user_genres):
        user_genres['기타'] = 100 - temp

    user_genre_names = []
    user_genre_percent = []
    for g in user_genres.keys():
        user_genre_names.append(g)
        user_genre_percent.append(user_genres[g])

    context = {
        'user_movies': user_movies,
        'user_genre_names': user_genre_names,
        'user_genre_percent': user_genre_percent,
        'user_review_ids': user_review_ids,
        'movies_count': len(user_movies)
    }

    return Response(context)