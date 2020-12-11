from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
# from django.http import Http404
from django.template import loader
from django.urls import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    # return HttpResponse("Hello, world. You’re at the polls index")

def detail(request, question_id):
    # 상위 계층에서 ObjectDoesNotExist 예외를 자동으로 잡아 내는 대신 get_object_or_404() 도움 함수(helper functoin) 또는 Http404를 사용하는 이유: 모델 계층을 뷰 계층에 연결하는 방법이기 때문.  Django의 중요한 설계 목표는, 약결합(loose coupling)을 관리하는 데에 있다.
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})
    
    # return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)

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
