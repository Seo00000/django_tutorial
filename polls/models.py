import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)  # 필수인수 max_length
    pub_date = models.DateTimeField('date published')  # Field 클래스의 생성자에 선택적인 첫번째 위치 인수를 전달하여 사람이 읽기 좋은(human-readable) 이름을 지정
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now  # 최근 하루(지금이거나 이전이고 하루 전보다는 적은, 시간이 덜 지난)
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 각각의 Choice 가 하나의 Question 에 관계된다는 것
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
