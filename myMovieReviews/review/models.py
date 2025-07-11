from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='장르명')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '장르'
        verbose_name_plural = '장르들'

class Review(models.Model):
    title = models.CharField(max_length=100, verbose_name='영화 제목')
    year = models.PositiveIntegerField(verbose_name='개봉연도', blank=True, null=True)
    director = models.CharField(max_length=50, verbose_name='감독')
    main_actor = models.CharField(max_length=50, verbose_name='주연')
    genre = models.ManyToManyField(Genre, verbose_name='장르')
    rating = models.PositiveSmallIntegerField(verbose_name='별점', choices=[(i, str(i)) for i in range(1, 6)])
    running_time = models.PositiveIntegerField(verbose_name='러닝타임(분)')
    content = models.TextField(verbose_name='리뷰 내용')
    image = models.ImageField(upload_to='review_images/', blank=True, null=True, verbose_name='포스터 이미지')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    def __str__(self):
        return f'{self.title} ({self.director}) - {self.rating}점'
