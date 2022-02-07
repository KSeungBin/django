from django.urls import path
from voting2 import views
app_name = 'voting2'
urlpatterns = [
# /voting2/
path('', views.index, name='index'),    # default값 그대로 url로 사용하므로 '' + views.py에 정의된 views.index를 url name으로 가져옴 + index.html과 mapping
# /voting2/5/
path('<int:question_id>/', views.detail, name='detail'), # int인지 str인지 정의해줘야 함 + views.py의 pk로 정의된 q_id를 가져옴 + detail.html과 mapping
# /voting2/5/results/
path('<int:question_id>/results/', views.results, name='results'),
# /voting2/5/vote/
path('<int:question_id>/vote/', views.vote, name='vote'),
]
