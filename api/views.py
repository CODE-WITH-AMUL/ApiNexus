from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import PublicAPI, Category, Tag
from django.views.generic import ListView, DetailView


def home(request):
    """Homepage view with all APIs, filtering, and pagination"""
    # Get all APIs
    apis = PublicAPI.objects.all().select_related('category').prefetch_related('tags')
    
    # Get all categories with API counts
    categories = Category.objects.annotate(api_count=Count('apis')).order_by('-api_count')
    
    # Get trending APIs (most recently added)
    trending_apis = apis.order_by('-created_at')[:6]
    
    # Handle search
    query = request.GET.get('q', '')
    if query:
        apis = apis.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(meta_description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Handle category filter
    category_slug = request.GET.get('category')
    if category_slug:
        apis = apis.filter(category__slug=category_slug)
    
    # Handle authentication filter
    auth_type = request.GET.get('auth')
    if auth_type:
        apis = apis.filter(auth=auth_type)
    
    # Handle free filter
    if request.GET.get('is_free') == '1':
        apis = apis.filter(is_free=True)
    
    # Handle HTTPS filter
    if request.GET.get('https'):
        apis = apis.filter(https_support=True)
    
    # Handle CORS filter
    if request.GET.get('cors'):
        apis = apis.filter(cors=True)
    
    # Sort options
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by == 'name':
        apis = apis.order_by('name')
    elif sort_by == 'free':
        apis = apis.order_by('-is_free', 'name')
    else:
        apis = apis.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(apis, 12)  # Show 12 APIs per page
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
    
    return render(request, 'home.html', context)


class APIDetailView(DetailView):
    """Detailed view for a single API"""
    model = PublicAPI
    template_name = 'api/detail.html'
    context_object_name = 'api'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related APIs
        context['related_apis'] = PublicAPI.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context


class CategoryListView(ListView):
    """List all categories"""
    model = Category
    template_name = 'api/categories.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(api_count=Count('apis')).order_by('name')


class TagListView(ListView):
    """List all tags"""
    model = Tag
    template_name = 'api/tags.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        return Tag.objects.annotate(api_count=Count('apis')).order_by('name')