from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

# class Profile(User):
#     avatar = models.URLField(max_length=256, verbose_name='Аватар')

#     def __str__(self):
#         return self.username

#     class Meta:
#         verbose_name = 'Профиль'
#         verbose_name_plural = 'Профили'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField(max_length=256, verbose_name='Аватар')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class LikeDislikeManager(models.Manager):
    def likes(self):
        return self.get_queryset().filter(vote__gt=0)
 
    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)
 
    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTE = [
        (LIKE, 'Нравится'),
        (DISLIKE, 'Не нравится')
    ]
    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTE)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeDislikeManager()

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-date_create')
    def hot(self):
        return self.order_by('-rating')
    def sort_by_tag(self, tag):
        return self.filter(tags__name__exact=tag)


class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст вопроса')

    tags = models.ManyToManyField('Tag', verbose_name='Теги вопроса')
    profile_asked = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Профиль который спрашивает')

    likes = GenericRelation(LikeDislike, related_query_name='questions')

    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField(default=0)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    objects = QuestionManager()

class Answer(models.Model):
    text = models.TextField(verbose_name='Текст ответа')
    correct = models.BooleanField(default=False, verbose_name='Ответ верный') 
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    profile_answered = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Профиль который отвечает')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    rating = GenericRelation(LikeDislike, related_query_name='Answers')


    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'











