from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import PublicAPI, Category, Tag
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

def home(request):
    """Homepage view with all APIs, filtering, and pagination"""
    apis = PublicAPI.objects.all().select_related('category').prefetch_related('tags')

    # Categories
    categories = Category.objects.annotate(api_count=Count('apis')).order_by('-api_count')

    # Trending APIs
    trending_apis = apis.order_by('-created_at')[:6]

    # Search
    query = request.GET.get('q', '')
    if query:
        apis = apis.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(meta_description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    # Filters
    category_slug = request.GET.get('category')
    if category_slug:
        apis = apis.filter(category__slug=category_slug)

    auth_type = request.GET.get('auth')
    if auth_type:
        apis = apis.filter(auth=auth_type)

    if request.GET.get('is_free') == '1':
        apis = apis.filter(is_free=True)

    # Sorting
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by == 'name':
        apis = apis.order_by('name')
    elif sort_by == 'free':
        apis = apis.order_by('-is_free', 'name')
    else:
        apis = apis.order_by('-created_at')

    # Pagination
    paginator = Paginator(apis, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'apis': page_obj,
        'categories': categories,
        'trending_apis': trending_apis,
        'query': query,
        'total_apis': apis.count(),
        'category_slug': category_slug,
        'auth_type': auth_type,
        'page_obj': page_obj,
    }

    return render(request, 'screen/home.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = 'api/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(api_count=Count('apis')).order_by('name')


class TagListView(ListView):
    model = Tag
    template_name = 'api/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.annotate(api_count=Count('apis')).order_by('name')



@login_required(login_url='login')
def ViewAPi(request, slug):
    """API detail page"""
    api = get_object_or_404(PublicAPI, slug=slug)
    context = {
        'api': api
    }
    return render(request, 'pages/apis.html', context)
