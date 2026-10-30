from django.urls import path

from blog.views import (
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostDetailView,
    BlogPostListView,
    BlogPostUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blog_list"),
    path("create/", BlogPostCreateView.as_view(), name="blog_create"),
    path("<int:pk>/", BlogPostDetailView.as_view(), name="blog_detail"),
    path("<int:pk>/edit/", BlogPostUpdateView.as_view(), name="blog_update"),
    path("<int:pk>/delete/", BlogPostDeleteView.as_view(), name="blog_delete"),
]
