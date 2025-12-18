from django.shortcuts import render
from django.db.models import Q
from .models import PublicAPI


def apis(request):
    query = request.GET.get('q')

    category = request.GET.get('category')
    auth = request.GET.get('auth')
    is_free = request.GET.get('is_free')

    apis = (
        PublicAPI.objects
        .filter(is_active=True, is_free=True)
        .select_related('category')
        .prefetch_related('tags')
    )

    # Global search
    if query:
        apis = apis.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    # Filters
    if category:
        apis = apis.filter(category__slug=category)

    if auth:
        apis = apis.filter(auth=auth)

    if is_free:
        apis = apis.filter(is_free=True)

    context = {
        'apis': apis,
        'query': query,
    }

    return render(request, 'content/apis.html', context)
