from django.contrib import admin
from polls.models import Question, Choice


class ChoiceInline(admin.StackedInline):
    # ctrl 키 누르고 StackedInline (Class) 클릭하면 정의된 속성 알 수 있음
    model = Choice
    extra = 2 # 브라우저를 열어보면 choice #1, choice #2 -> 2개가 default로 한 화면에 생성됨


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        # ('Question Statement', {'fields' : ['question_text']}),
        (None, {'fields': ['question_text']}), # None = Question Statement라는 목차가 사라짐
        ('Date Information', {'fields': [
         'pub_date'], 'classes': ['collapse']}), # collapse는 내용이 감춰짐 -> 내가 클릭을 해야 데이터가 보임
    ]
    inlines = [(ChoiceInline)] # add Choice 클래스(model.py에 정의된) 같이 보이도록 함
    list_display = ('question_text', 'pub_date') # 레코드 리스트 컬럼 지정
    list_filter = ['pub_date'] # list_display부터 search_fields까지는 admin 페이지의 '변경' 버튼을 누르면 확인할 수 있음
    search_fields = ['question_text']

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)   # 클래스를 admin에도 등록해줌
