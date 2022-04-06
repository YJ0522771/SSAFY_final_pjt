from django.db import models

class Genre(models.Model):
    tmdb_id = models.IntegerField()
    name = models.CharField(max_length=30)


class Movie(models.Model):
    tmdb_id = models.IntegerField()

    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.CharField(max_length=500)
    release_date = models.CharField(max_length=20)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    playing =  models.BooleanField(default=False)

    genres = models.ManyToManyField(Genre, related_name='genre_movies')


# class MovieComment(models.Model):
#     content = models.CharField(max_length=200)
#     vote = models.IntegerField()

#     movie = models.ForeignKey(Movie, on_delete=CASCADE, related_name='commented_movie')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='commented_user')
