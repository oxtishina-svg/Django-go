from typing import cast

from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.models import BlogPost


class BlogPostListView(ListView):
    """Отображает список опубликованных статей."""

    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[BlogPost]:
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Отображает отдельную статью."""

    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset: QuerySet[BlogPost] | None = None) -> BlogPost:
        post = cast(BlogPost, super().get_object(queryset))

        post.views_count += 1
        post.save(update_fields=["views_count"])

        return post


class BlogPostCreateView(CreateView):
    """Создаёт новую статью."""

    model = BlogPost
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )
    template_name = "blog/blog_form.html"

    def get_success_url(self) -> str:
        post = cast(BlogPost, self.object)

        return reverse(
            "blog:blog_detail",
            kwargs={"pk": post.pk},
        )


class BlogPostUpdateView(UpdateView):
    """Редактирует существующую статью."""

    model = BlogPost
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )
    template_name = "blog/blog_form.html"

    def get_success_url(self) -> str:
        post = cast(BlogPost, self.object)

        return reverse(
            "blog:blog_detail",
            kwargs={"pk": post.pk},
        )


class BlogPostDeleteView(DeleteView):
    """Удаляет статью."""

    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"

    def get_success_url(self) -> str:
        return reverse("blog:blog_list")
