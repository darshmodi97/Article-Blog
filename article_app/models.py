from datetime import date

from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    username = models.CharField(max_length=100, default='')
    DOB = models.DateField(default=date.today)
    gender = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    login_id = models.ForeignKey('Login',on_delete=models.CASCADE, default='')
    def __str__(self):
        return self.name



class Login(models.Model):

    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name


class Post_Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Post_Category'

    def __str__(self):
        return self.category_name


class Article(models.Model):

    heading = models.CharField(max_length=150)
    article_content = models.TextField()
    type = models.ForeignKey(Post_Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to= 'media')
    uploaded_on = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(Users, on_delete=models.CASCADE )

    def __str__(self):
        return self.heading

class Tags(models.Model):
    tags_title = models.TextField()

    def __str__(self):
        return self.tags_title

class Article_Tags(models.Model):

    tags = models.ForeignKey(Tags,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    class Meta :
        db_table = 'Article_Tags_mapping'

