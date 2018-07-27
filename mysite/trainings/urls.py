from django.urls import path
from . import views

urlpatterns =[
    path('', views.index,name='index'),
    path('search/',views.search,name='search'),
    path('<int:language_id>/', views.topics,name='topics'),
    path('<int:language_id>/<int:topic_id>/', views.posts, name='posts'),
    # path('<int:language_id>/<int:topic_id>/', views.PostView.as_view(), name='posts'),
    path('<int:language_id>/new/',views.new_topic, name ='new_topic'),
    path('<int:language_id>/<int:topic_id>/new/', views.new_post, name='new_post'),
    path('<int:language_id>/<int:topic_id>/<int:post_id>/', views.visit_post, name='visit_post'),
    path('myaccount/',views.my_account,name='my_account'),
    path('<int:language_id>/<int:topic_id>/<int:post_id>/comment/',views.new_comment,name='comment_post'),
    path('<int:language_id>/<int:topic_id>/<int:post_id>/feedback/',views.feedback_post,name='submit_feedback'),
]