from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        total_article_rating = 3 * sum(post.rating for post in self.post_set.all())
        total_comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        total_article_comments_rating = sum(comment.rating for post in self.post_set.all() for comment in
                                            Comment.objects.filter(user=self.user, post=post))
        self.rating = total_article_rating + total_comment_rating + total_article_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    POST_TYPES = [
        ('article', 'Статья'),
        ('news', 'Новость'),
    ]
    post_type = models.CharField(max_length=7, choices=POST_TYPES)
    time_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category, through='PostCategory')
    content = models.TextField()
    rating = models.FloatField(default=0.0)

    def preview(self):
        preview_length = 124
        if len(self.content) <= preview_length:
            return self.content
        else:
            return f"{self.content[:preview_length]}..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'category']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Comment by {self.user} on {self.post.title}"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
