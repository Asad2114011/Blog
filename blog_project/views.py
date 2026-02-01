from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from posts.models import Post
from catagories.models import catagory, Tag

def home(request, catagory_slug=None):
    # Filter posts by category if provided
    data = Post.objects.select_related('author', 'catagory').prefetch_related('tags', 'likes', 'comments')
    selected_category = None
    
    if catagory_slug is not None:
        selected_category = catagory.objects.get(slug=catagory_slug)
        data = data.filter(catagory=selected_category)
    
    # Pagination
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # All categories with post count
    catagories = catagory.objects.all()
    
    # Count all posts
    all_posts_count = Post.objects.count()
    
    # Trending posts (most liked in last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    trending_posts = Post.objects.filter(
        created_at__gte=thirty_days_ago
    ).annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:5]
    
    # Popular tags
    popular_tags = Tag.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:10]
    
    context = {
        'data': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'catagory': catagories,
        'selected_category': selected_category,
        'trending_posts': trending_posts,
        'popular_tags': popular_tags,
        'all_posts_count': all_posts_count,
    }
    
    return render(request, 'home.html', context)