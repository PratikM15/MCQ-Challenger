from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        code = request.POST['code']
        try:
            test = Test.objects.get(code=code)
        except:
            test = None
        try:
            student = Student.objects.get(email=email)
        except:
            student = None
        if student != None and student.test == test and student.completed:
            return render(request, 'index.html', {'error': 'You already completed the test.'})
        if test:
            student = Student(name=name, email=email, mobile=mobile, test=test, score=0)
            student.save()
            return render(request, 'rules.html', {'id':student.id, 'code': code})
        else:
            return render(request, 'index.html', {'error': 'Invalid Test Code'})
    return render(request, 'index.html')



def paper(request, id, code):
    student = Student.objects.get(id=id)
    if student.completed:
        return redirect('index')
    if request.method == "POST":
        studentid = request.POST['studentid']
        code = request.POST['testcode']
        student = Student.objects.get(id=studentid)
        test = Test.objects.get(code=code)
        ques = Question.objects.filter(test=test)
        score = 0
        for que in ques:
            que_name = str(que.id)
            que_answer = request.POST.get(que_name, None)
            if que_answer == que.answer:
                score += 1
            if que_answer == None:
                que_answer = "0"
            student_response = StudentResponse(student=student, test=test, question=que, answer=que_answer)
            student_response.save()
        if student.completed:
            return redirect('result', id, code)
        student.score = score
        student.completed = True
        student.save()
        return redirect('result', id, code)
    test = Test.objects.get(code=code)
    ques = Question.objects.filter(test=test)
    student = Student.objects.get(id=id)
    context = {'id':id, 'code': code, 'ques': ques, 'time': test.test_time}
    return render(request, 'paper.html', context)

def result(request, id, code):
    student = Student.objects.get(id=id)
    test = Test.objects.get(code=code)
    student_responses = StudentResponse.objects.filter(student=student)
    context = {"name": student.name, "code" : code, "score": student.score, 'responses': student_responses}
    text = "Dear " + student.name + " your score for the test " + code + " is " + student.score + " ."
    return render(request, 'result.html', context)

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def check_result(request):
    if request.method == "POST":
        email = request.POST['email']
        code = request.POST['code']
        try:
            student = Student.objects.get(email=email)
            return redirect('result', student.id, code)
        except:
            student = None
        return render(request, 'check.html', {'error': 'Invalid Details.'})
    return render(request, 'check.html')