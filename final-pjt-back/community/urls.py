from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('<int:movie_id>/', views.review_list),
    path('<int:movie_id>/create/', views.review_create),
    path('<int:review_id>/detail/', views.review_detail),
    path('<int:review_id>/putdelete/', views.review_put_delete),
    path('<int:review_id>/comment/', views.comment_list),
    path('<int:review_id>/comment/create/', views.comment_create),
    path('comment/<int:comment_id>/delete/', views.comment_delete)
]