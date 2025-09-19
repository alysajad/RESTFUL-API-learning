from django.urls import include, path
from .import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('employees', views.EmployeeViewSet, basename='employees')  #class based viewset

urlpatterns = [
    path('students/',views.studentsView),
    path('students/<int:pk>/',views.studentDetailView),
   ## path('employees/',views.Employees.as_view()),
   ## path('employees/<int:pk>/',views.EmployeeDetail.as_view()),
   path('', include(router.urls)),
   path('blogs/', views.BlogsView.as_view()),  # List and create blogs
   path('comments/', views.CommentsView.as_view()),  # List and create comments
path('comments/<int:pk>/', views.CommentDetailView.as_view()),  # Retrieve, update, delete a comment
   path('blogs/<int:pk>/', views.BlogDetailView.as_view()),  # Retrieve, update, delete a blog
]