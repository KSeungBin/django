from django.db import models

# Create your models here.


class Question(models.Model):  # jango.db의 models를 상속받아 question class 생성
    # id 필드(primary key)는 django에서 자동 생성되므로 속성 정의해줄 필요 없음
    question_text = models.CharField(max_length=200) # DB에 쌓일 데이터
    pub_date = models.DateTimeField('date published') # 작성 날짜

    def __str__(self):   # 전달인자를 자신으로 받은 것(Question): 메서드 정의
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
