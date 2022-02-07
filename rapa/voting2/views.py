from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from voting2.models import Choice, Question

# Create your views here.
# 현재는 함수 형태로 view가 저장되어있지만, 클래스 형태로 바꿀 수도 있음


def index(request):  # 사용자의 request를 받음
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]  # 5개의 requests를 최신 질문 목록에 저장
    context = {'latest_question_list': latest_question_list} # list 형태로 context에 저장
    return render(request, 'voting2/index.html', context)  # index.html파일을 template으로 해서 context를 받아 for문 돌리면서 데이터를 rendering(= html파일을 만듦)함
                                                           # index.html에서 rendering이 일어나는 것


def detail(request, question_id):  
    question = get_object_or_404(Question, pk=question_id)  # return 결과값을 question이 받음. (고유키ㅅ(primary)으로 query를 만듦)
    return render(request, 'voting2/detail.html', {'question': question}) # client의 request; template; 반환 결과값이 저장된 question을 이 형태로 넣어주면 detail page가 생성됨
# detail: 질문을 클릭하면 나오는 세부항목 페이지 by q_id를 DB(Question) 에서 찾아 question 변수에 넘겨주어, 값이 있으면 dict type의 value에 저장하여 template을 가지고 rendering

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'voting2/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })  
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('voting2:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'voting2/results.html', {'question': question})

