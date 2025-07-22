from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login
import json
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like, Story
from .forms import PostForm, SignUpForm, StoryForm


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:feed')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


@login_required
def toggle_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        Like.objects.create(post=post, user=user)

        like_count = post.like_set.count()

        return JsonResponse({'like_count': like_count})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        data = json.loads(request.body)
        content = data.get('content')

        if content:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            return JsonResponse({
                'status': 'ok',
                'comment': {
                    'id': comment.id,
                    'author': comment.author.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                }
            })
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author == request.user:
            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)
    return JsonResponse({'status': 'error'}, status=400)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('posts:feed')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')

    recent_story_users_ids = Story.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=1)
    ).values_list('author__id', flat=True).distinct()
    story_users = User.objects.filter(id__in=recent_story_users_ids)

    form = PostForm()
    context = {
        'posts': posts,
        'story_users': story_users,
        'form': form,
    }
    return render(request, 'feed.html', context)

@login_required
def get_user_stories(request, user_id):
    stories = Story.objects.filter(
        author_id=user_id,
        created_at__gte=timezone.now() - timedelta(days=1)
    ).order_by('created_at')

    story_data = [{'image_url': story.image.url} for story in stories]
    return JsonResponse(story_data, safe=False)

@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.expires_at = timezone.now() + timedelta(days=1)
            story.save()
            return redirect('posts:feed')
    else:
        form = StoryForm()
    return render(request, 'story_form.html', {'form': form})