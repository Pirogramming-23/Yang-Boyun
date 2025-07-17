from django.shortcuts import render, redirect, get_object_or_404
from .forms import IdeaForm, DevToolForm
from .models import DevTool, Idea, IdeaStar
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

# Create your views here.

def main(request):
    q = request.GET.get('q', '')
    devtool_id = request.GET.get('devtool', '')
    sort = request.GET.get('sort', 'latest')
    idea_list = Idea.objects.all()
    if q:
        idea_list = idea_list.filter(title__icontains=q)
    if devtool_id:
        idea_list = idea_list.filter(devtool_id=devtool_id)
    
    # 정렬 처리
    if sort == 'latest':
        idea_list = idea_list.order_by('-created_at')
    elif sort == 'oldest':
        idea_list = idea_list.order_by('created_at')
    elif sort == 'name':
        idea_list = idea_list.order_by('title')
    elif sort == 'interest':
        idea_list = idea_list.order_by('-interest')
    else:
        idea_list = idea_list.order_by('-created_at')  # 기본값
    
    paginator = Paginator(idea_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    devtools = DevTool.objects.all() # type: ignore
    
    # 세션에서 찜한 아이디어 목록 가져오기
    starred_ideas = request.session.get('starred_ideas', [])
    
    for idea in page_obj:
        idea.is_starred = idea.pk in starred_ideas
    
    return render(request, 'ideas/main.html', {
        'ideas': page_obj,
        'page_obj': page_obj,
        'q': q,
        'devtool_id': devtool_id,
        'sort': sort,
        'devtools': devtools,
    })

def create_idea(request):
    devtools = DevTool.objects.all()
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            devtool_name = form.cleaned_data.get('devtool_input')
            if devtool_name:
                devtool_obj, _ = DevTool.objects.get_or_create(name=devtool_name)
                idea.devtool = devtool_obj
            idea.save()
            return redirect(idea_detail, pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'ideas/create.html', {'form': form, 'devtools': devtools})

def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm()
    return render(request, 'ideas/devtool_create.html', {'form': form})

def devtool_list(request):
    devtools = DevTool.objects.all() # type: ignore
    return render(request, 'ideas/devtool_list.html', {'devtools': devtools})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    # 세션에서 찜한 아이디어 목록 가져오기
    starred_ideas = request.session.get('starred_ideas', [])
    idea.is_starred = idea.pk in starred_ideas
    
    return render(request, 'ideas/detail.html', {'idea': idea})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    devtools = DevTool.objects.all()
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save(commit=False)
            devtool_name = form.cleaned_data.get('devtool_input')
            if devtool_name:
                devtool_obj, _ = DevTool.objects.get_or_create(name=devtool_name)
                idea.devtool = devtool_obj
            idea.save()
            return redirect(idea_detail, pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
        # 기존 devtool 값 설정
        if idea.devtool:
            form.fields['devtool_input'].initial = idea.devtool.name
    return render(request, 'ideas/update.html', {'form': form, 'idea': idea, 'devtools': devtools})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        idea.delete()
        return redirect('main')
    return render(request, 'ideas/delete_confirm.html', {'idea': idea})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    ideas = Idea.objects.filter(devtool=devtool) # type: ignore
    return render(request, 'ideas/devtool_detail.html', {'devtool': devtool, 'ideas': ideas})

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, 'ideas/devtool_update.html', {'form': form, 'devtool': devtool})

def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        devtool.delete()
        return redirect('devtool_list')
    return render(request, 'ideas/devtool_delete_confirm.html', {'devtool': devtool})

def toggle_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    
    # 세션에서 찜한 아이디어 목록 가져오기
    starred_ideas = request.session.get('starred_ideas', [])
    
    if pk in starred_ideas:
        # 이미 찜한 경우 제거
        starred_ideas.remove(pk)
        starred = False
    else:
        # 찜하지 않은 경우 추가
        starred_ideas.append(pk)
        starred = True
    
    # 세션에 저장
    request.session['starred_ideas'] = starred_ideas
    
    # 찜 개수는 세션 기반으로 계산
    star_count = len(starred_ideas)
    
    return JsonResponse({'starred': starred, 'star_count': star_count})

@require_POST
def adjust_interest(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    action = request.POST.get('action')
    if action == 'up':
        idea.interest += 1
    elif action == 'down' and idea.interest > 0:
        idea.interest -= 1
    idea.save()
    return JsonResponse({'interest': idea.interest})

@csrf_exempt
def idea_search(request):
    q = request.GET.get('q', '')
    devtool_id = request.GET.get('devtool', '')
    idea_list = Idea.objects.all() # type: ignore
    if q:
        idea_list = idea_list.filter(title__icontains=q)
    if devtool_id:
        idea_list = idea_list.filter(devtool_id=devtool_id)
    paginator = Paginator(idea_list.order_by('-created_at'), 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 세션에서 찜한 아이디어 목록 가져오기
    starred_ideas = request.session.get('starred_ideas', [])
    
    for idea in page_obj:
        idea.is_starred = idea.pk in starred_ideas
    
    html = render_to_string('ideas/_idea_cards.html', {'ideas': page_obj, 'user': request.user})
    pagination_html = render_to_string('ideas/_pagination.html', {'page_obj': page_obj, 'q': q, 'devtool_id': devtool_id})
    return JsonResponse({'html': html, 'pagination_html': pagination_html})
