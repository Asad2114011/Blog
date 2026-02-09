from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from posts.models import Post,Like,Comment,Bookmark
from author.models import Author
from catagories.models import catagory, Tag
from django.contrib.auth.decorators import login_required 

def home(request, catagory_slug=None):
    data=Post.objects.select_related('author','catagory').prefetch_related('tags','likes','comments')
    selected_category = None
    query = request.GET.get('q', '')
    
    if query:
        data = data.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__name__icontains=query) |
            Q(catagory__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Category filter
    if catagory_slug is not None:
        selected_category = catagory.objects.get(slug=catagory_slug)
        data = data.filter(catagory=selected_category)
    
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    catagories = catagory.objects.all()
    
    all_posts_count = Post.objects.count()
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    trending_posts = Post.objects.filter(
        created_at__gte=thirty_days_ago
    ).annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:5]
    
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
        'query': query,  # Add query to context
    }
    
    return render(request, 'home.html', context)


@login_required
def favourites(request):
    author = request.user.author_profile
    bookmarks = Bookmark.objects.filter(user=author).select_related('post__author', 'post__catagory').prefetch_related('post__tags')
    
    # Get only the posts from bookmarks
    bookmarked_posts = [bookmark.post for bookmark in bookmarks]
    
    # Pagination
    paginator = Paginator(bookmarked_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'data': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'favourites.html', context)


def search(request):
    query = request.GET.get('q', '')
    
    posts = []
    authors = []
    categories = []
    tags = []
    
    if query:
        # Search posts
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
        
        # Search authors
        authors = Author.objects.filter(
            Q(name__icontains=query) |
            Q(bio__icontains=query)
        ).distinct()
        
        # Search categories
        categories = catagory.objects.filter(name__icontains=query)
        
        # Search tags
        tags = Tag.objects.filter(name__icontains=query)
    
    # Pagination for posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'posts': page_obj,
        'authors': authors,
        'categories': categories,
        'tags': tags,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'search_result.html', context)

def all_categories(request):
    categories = catagory.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')
    
    context = {
        'categories': categories,
    }
    return render(request, 'all_categories.html', context)

def all_authors(request):
    authors = Author.objects.annotate(post_count=Count('posts')).order_by('-post_count')
    
    paginator = Paginator(authors, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'authors': authors,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'all_authors.html', context)

def all_tags(request):
    tags = Tag.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')
    
    context = {
        'tags': tags,
    }
    return render(request, 'all_tags.html', context)

def users_profile(request,slug):
    author=get_object_or_404(Author,slug=slug)
    posts=Post.objects.filter(author=author)
    return render(request,'users_profile.html',{'posts':posts,'author':author})
