
from django.db import models

class Student(models.Model):
    reg_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    grade_history_chart = models.JSONField(null=True,blank=True)
    def __str__(self):
        return f'{self.name} {self.id}'



class MCQ(models.Model):
    title = models.CharField(max_length=200)
    mcq_id=models.AutoField(primary_key=True)
    def __str__(self):
        return f"{self.title} - {self.mcq_id}"


class Question(models.Model):
    mcq = models.ForeignKey(MCQ, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    options = models.JSONField()  # JSON field to store options as a dictionary, e.g., {"A": "Option1", "B": "Option2", ...}
    correct_answer = models.CharField(max_length=1)  # Store the correct answer as a key like "A", "B"

    def __str__(self):
        return f"Question: {self.question_text} (MCQ ID: {self.mcq.mcq_id})"


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.teacher_id}'
class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(Student, related_name='classes')

    def __str__(self):
        return f'{self.name} {self.class_id}'
