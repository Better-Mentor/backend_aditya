
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student, MCQ, Teacher, Class,Question
from .serializers import StudentSerializer, MCQSerializer, TeacherClassSerializer, StudentInClassSerializer
from .mcq_analyzer import MCQAnalyzer
analyzer = MCQAnalyzer()
@api_view(['POST'])
def student_dashboard(request):
    reg_no = request.data.get('RegNo')
    student = Student.objects.filter(reg_no=reg_no).first()
    if not student:
        return JsonResponse({'error': 'Student not found'}, status=404)

    mcq_ids = list(MCQ.objects.values_list('mcq_id', flat=True))
    response_data = {
        'Student name': student.name,
        'Grade History Chart': student.grade_history_chart,
        'mcqIDs': mcq_ids
    }
    return JsonResponse(response_data)

@api_view(['POST'])
def take_mcq(request):
    reg_no = request.data.get('RegNo')
    mcq_id = request.data.get('mcqID')

    # Retrieve the MCQ by ID
    mcq = MCQ.objects.filter(mcq_id=mcq_id).first()
    if not mcq:
        return Response({"error": "MCQ not found"}, status=404)

    # Gather all questions for the MCQ
    questions_data = []
    questions = mcq.questions.all()  # Retrieve all Question objects related to the MCQ
    for question in questions:
        questions_data.append({
            'question_id': question.id,
            'question': question.question_text,
            'options': question.options  # Returns options as a dictionary
        })

    # Construct response data
    response_data = {
        'mcq_id': mcq.mcq_id,
        'title': mcq.title,
        'questions': questions_data
    }

    return Response(response_data)

@api_view(['POST'])
def analyze_mcq(request):

    
    reg_no = request.data.get('RegNo')
    mcq_id = request.data.get('McqID')
    student_answers = request.data.get('answers')  # Array of student's answers

    # Retrieve the MCQ and its questions
    mcq = MCQ.objects.filter(mcq_id=mcq_id).first()
    if not mcq:
        return Response({"error": "MCQ not found"}, status=404)

    # Prepare analysis data
    analysis_data = []
    questions = mcq.questions.all()
    for idx, question in enumerate(questions):
        options=[]
        for _,k in question.options.items():
            options.append(k)
        analysis_data.append({
            'question': question.question_text,
            'correct_answer': question.correct_answer,
            'student_answer': question.options[student_answers[idx]],  # Student's answer from the request
            'options': options  # List of options
        })
    print(analysis_data)
    results = analyzer.analyze_test_performance(analysis_data)

    return Response({"analysis_data": results})


@api_view(['GET'])
def all_classes(request, teacherid):
    classes = Class.objects.filter(teacher__teacher_id=teacherid)
    serializer = TeacherClassSerializer(classes, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def class_details(request, classID):
    class_obj = Class.objects.filter(class_id=classID).first()
    if not class_obj:
        return JsonResponse({'error': 'Class not found'}, status=404)

    students = class_obj.students.all()
    serializer = StudentInClassSerializer(students, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def student_details(request, studentID):
    # Placeholder logic - replace with logic for retrieving and averaging student scores
    response_data = {
        'Avg score of class': 75,  # Placeholder value
        'Student score of 4 previous tests': [80, 70, 85, 65]
    }
    return JsonResponse(response_data)

@api_view(['POST'])
def upload_mcq(request):
    title = request.data.get('title')
    questions_data = request.data.get('questions')  # Array of questions with options and correct answers

    # Create MCQ instance
    mcq = MCQ.objects.create(title=title)

    # Add each question to the MCQ
    for q_data in questions_data:
        question_text = q_data['question']
        options = q_data['options']  # Should be a dictionary, e.g., {"A": "Option1", "B": "Option2", ...}
        correct_answer = q_data['correct_answer']  # Correct answer key, e.g., "A"

        # Create a Question instance linked to the MCQ
        Question.objects.create(
            mcq=mcq,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer
        )

    return Response({"message": "MCQ uploaded successfully", "mcq_id": mcq.mcq_id})

