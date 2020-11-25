from django.db import models

# Create your models here.
class Test(models.Model):
    code = models.CharField(max_length=5)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    test_time = models.CharField(max_length=3, default=None)

    def __str__(self):
        return self.code

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    score = models.CharField(max_length=3)
    completed = models.BooleanField(default=False)
    remaining_time = models.CharField(default="60", max_length=3)

    def __str__(self):
        return self.name + " " + str(self.test.code)

class Question(models.Model):
    question = models.CharField(max_length=500)
    choice1 = models.CharField(max_length=500)
    choice2 = models.CharField(max_length=500)
    choice3 = models.CharField(max_length=500)
    choice4 = models.CharField(max_length=500)
    answer = models.CharField(max_length=1)
    test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.question

class StudentResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1)
    test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.student.name + " " + str(self.test.code)