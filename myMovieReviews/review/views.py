from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Genre
from .forms import ReviewForm

# 리뷰 리스트
def review_list(request):
    sort = request.GET.get('sort')
    if sort == 'title':
        reviews = Review.objects.all().order_by('title')
    elif sort == 'rating':
        reviews = Review.objects.all().order_by('-rating')
    elif sort == 'running_time':
        reviews = Review.objects.all().order_by('-running_time')
    else:
        reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'review_list.html', {'reviews': reviews, 'request': request})

# 리뷰 디테일
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'review_detail.html', {'review': review})

# 리뷰 작성
def review_create(request):
    genres = Genre.objects.all()
    form = ReviewForm(request.POST or None, request.FILES or None)
    errors = None
    if request.method == 'POST':
        if form.is_valid():
            review = form.save(commit=False)
            review.year = request.POST.get('year')
            review.save()
            review.genre.set(request.POST.getlist('genre'))
            return redirect('review_list')
        else:
            errors = form.errors
    return render(request, 'review_create.html', {'form': form, 'genres': genres, 'errors': errors})

# 리뷰 수정
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    genres = Genre.objects.all()
    if request.method == 'POST':
        # 사진 없애기 버튼이 눌렸을 때
        if 'remove_image' in request.POST:
            if review.image:
                review.image.delete(save=False)
                review.image = None
                review.save()
            return redirect('review_update', pk=review.pk)
        form = ReviewForm(request.POST, request.FILES, instance=review)
        print(form.errors)  # 폼 에러 콘솔 출력
        if form.is_valid():
            review = form.save(commit=False)
            review.year = request.POST.get('year')
            review.save()
            review.genre.set(request.POST.getlist('genre'))
            return redirect('review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review_update.html', {'form': form, 'review': review, 'genres': genres})

# 리뷰 삭제
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'review_delete.html', {'review': review})
