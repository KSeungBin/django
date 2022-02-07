from django.views.generic.base import TemplateView
# class형 : url과 연결되는 view를 클래스로 정의
# home.html 파일은 class를 generic.base의 templateview에서 상속 받는다

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_list'] = ['polls', 'voting2'] # view를 class 형태로 받음을 알 수 있다.
        return context
