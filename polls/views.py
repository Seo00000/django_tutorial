from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
    # 제너릭 뷰에 대한 문서 https://docs.djangoproject.com/ko/3.1/topics/class-based-views/
    template_name = 'polls/index.html'  #  Django에게 자동 생성 된 기본 템플릿 이름 대신에 특정 템플릿 이름을 사용하도록 알려주기 위해 사용됨.
    context_object_name = 'latest_question_list'

     def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        # timezone.now보다 pub_date가 작거나 같은 Question을 포함하는 queryset을 반환함.
        # sql의 where, 기본형태: field__lookuptype=value  # http://recordingbetter.com/django/2017/06/07/Django-ORM
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]  # 내림차순, DESC
    #     https://ssungkang.tistory.com/entry/Django-ORM-Cookbook-%EC%A1%B0%ED%9A%8C-%EA%B2%B0%EA%B3%BC%EB%A5%BC-%EC%A0%95%EB%A0%AC%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  
        # request.POST 는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체, 항상 문자열들로 반환함.
        # POST 자료에 해당 값이 없으면 KeyError가 일어난다. 
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
        # reverse() 함수는 뷰 함수에서 URL을 하드코딩하지 않도록 도와준다. 제어를 전달하길 위하는 뷰의 이름을, URL 패턴의 변수 부분을 조합해서 해당 뷰를 가리킨다.
        # ex) 해당 구문은 '/polls/3/results/' 와 같은 구문을 반환함
    # return HttpResponse("You're voting on question %s." % question_id)
