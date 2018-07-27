from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    language = models.CharField(max_length=200)

    def __str__(self):
        return (self.language)

class Topic(models.Model):
    name = models.CharField(max_length=200,)
    language = models.ForeignKey(Language,related_name='topics',on_delete=models.CASCADE)

    def __str__(self):
        return (self.name)
    class Meta:
        unique_together = (('name','language'),)

class Post(models.Model):
    topic = models.ForeignKey(Topic,related_name='posts',on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500,default='')
    views = models.PositiveIntegerField(default=0)
    pdf_file = models.FileField(upload_to='uploads/')
    
    def __str__(self):
        return (self.title)

class Comments(models.Model):
    message = models.CharField(max_length=200)
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    commented_by =models.ForeignKey(User,on_delete=models.CASCADE)
    commented_on =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.message)

class Feedback(models.Model):
    feedback = models.CharField(max_length=500,null=True)
    rating = models.PositiveIntegerField()
    avg_rating = models.DecimalField(max_digits=2,decimal_places=1,default=0)
    rated_by = models.ForeignKey(User,related_name='users',on_delete=models.CASCADE)
    rated_post = models.ForeignKey(Post,related_name='posts',on_delete=models.CASCADE)
    rated_on = models.DateTimeField(auto_now_add=True,)

    class Meta:
        unique_together = (('rated_by','rated_post'),)