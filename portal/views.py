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
        password = request.POST['password']
        try:
            test = Test.objects.get(code=code)
            if test.active == False:
                return render(request, 'index.html', {'error': 'Inactive Test'})
        except:
            test = None
        try:
            student = Student.objects.get(email=email)
        except:
            student = None
        if student != None and student.test == test and student.completed:
            return render(request, 'index.html', {'error': 'You already completed the test.'})
        if student != None and student.test == test and student.completed==False:
            return render(request, 'rules.html', {'id':student.external_id, 'code': code})
        if test:
            student = Student(name=name, email=email, mobile=mobile, test=test, score=0, password=password)
            student.save()
            return render(request, 'rules.html', {'id':student.external_id, 'code': code})
        else:
            return render(request, 'index.html', {'error': 'Invalid Test Code'})
    return render(request, 'index.html')



def paper(request, external_id, code):
    student = Student.objects.get(external_id=external_id)
    if student.completed:
        return redirect('index')
    if request.method == "POST":
        studentid = request.POST['studentid']
        code = request.POST['testcode']
        student = Student.objects.get(external_id=studentid)
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
            return redirect('result', external_id, code)
        student.score = score
        student.completed = True
        student.save()
        return redirect('result', external_id, code)
    test = Test.objects.get(code=code)
    ques = Question.objects.filter(test=test)
    student = Student.objects.get(external_id=external_id)
    context = {'id':external_id, 'code': code, 'ques': ques, 'time': test.test_time}
    return render(request, 'paper.html', context)

def result(request, external_id, code):
    student = Student.objects.get(external_id=external_id)
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
        password = request.POST['password']
        try:
            student = Student.objects.get(email=email)
            if student.password == password:
                return redirect('result', student.external_id, code)
        except:
            student = None
        return render(request, 'check.html', {'error': 'Invalid Details.'})
    return render(request, 'check.html')

def check_scores(request):
    if request.method == "POST":
        code = request.POST['code']
        try:
            test = Test.objects.get(code=code)
            if test.active:
                return render(request, 'check_scores.html', {'error':'Test is in Progress. Wait until the test is over.'})
            total = len(Question.objects.filter(test=test))
            students = Student.objects.filter(test=test).order_by('-score')
            return render(request, 'scores.html', {'students': students, 'code': code, 'total': total})
        except Exception as e:
            return render(request, 'check_scores.html', {'error':'Invalid Test Code.'})
    return render(request, 'check_scores.html')
