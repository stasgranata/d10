from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        Summary = 0
        sample = self.post_set.all()

        for i in sample:
            Summary += 3 * i.rating
            sum_com = 0
            sub_sample = i.comment_set.all()
            for j in sub_sample:
                sum_com += j.rating
            Summary += sum_com
        sample = self.user.comment_set.all()

        for i in sample:
            Summary += i.rating

        self.rating = Summary
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    is_article = models.BooleanField(default=False)
    title = models.CharField(max_length=63)
    time_in = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default="Место для текста")
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.content) < 125:
            prw = self.content
        else:
            prw = self.content[:124] + '...'
        return prw

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

    def get_absolute_url(self):
        if self.is_article:
            return reverse('articles_detail', args=[str(self.id)])
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    reply = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
