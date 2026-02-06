from typing import Any

from blog.models import Page, Post, Tag
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView

PER_PAGE = 9


class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()  # type: ignore

    # def get_queryset(self) -> QuerySet[Any]:
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset


class CreatedByListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']

        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = f'Autor {user_full_name} - '

        ctx.update({
            'page_title': page_title
        })

        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['author_pk'])
        return qs


    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_title = f'Cat: {self.object_list[0].category.name} - ' # type: ignore

        ctx.update({
            'page_title': page_title
        })

        return ctx


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        tag = Tag.objects.filter(slug=self.kwargs.get('slug')).first()
        page_title = f'Tag: {tag.name} - '  # type: ignore

        ctx.update({
            'page_title': page_title
        })

        return ctx

# def tag(request, slug):
#     posts = Post.objects.get_published().filter(tags__slug=slug)  # type: ignore

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404

#     tag = Tag.objects.filter(slug=slug).first()
#     page_title = f'Tag: {tag.name} - '  # type: ignore

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published()  # type: ignore
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[0:PER_PAGE]
    )

    page_title = f'Busca: {search_value[:15]} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )


def page(request, slug):
    page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if page_obj is None:
        raise Http404

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': f'{page_obj.title} - ',  # type: ignore
        }
    )


def post(request, slug):
    post_obj = Post.objects.get_published().filter(slug=slug).first()  # type: ignore

    if post_obj is None:
        raise Http404

    page_title = f'Post: {post_obj.title[:15]} - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title
        }
    )
