from django.db import models
# ユーザー認証
from django.contrib.auth.models import User

class Account(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    pw_digest = models.CharField(max_length=130)
    def __str__(self):
        return self.user_name.username

class Genre(models.Model):
    genre_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.genre_name
    
class ControlMeasure(models.Model):
    cm_name = models.CharField(max_length=200)
    cm_contents = models.CharField(max_length=300, default="")
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.cm_name

class Report(models.Model):
    report_text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    cm_id = models.ForeignKey(ControlMeasure, on_delete=models.CASCADE, null=True, blank=True,)
    anonymous = models.BooleanField(default=False,)
    
    def __str__(self):
        return self.report_text

class Comment(models.Model):
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.comment_text
        
class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)
    like = models.IntegerField('Like',default=0)

class Bad(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)

class NGWord(models.Model):
    ng_words = models.CharField(max_length=30)
    def __str__(self):
        return self.ng_words
        
class KeyWord(models.Model):
    key_words = models.CharField(max_length=30)
    cm_id = models.ForeignKey(ControlMeasure, on_delete=models.CASCADE)
    def __str__(self):
        return self.key_words