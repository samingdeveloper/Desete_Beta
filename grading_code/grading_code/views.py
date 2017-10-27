from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ClassroomForm, QuizForm, UserForm
from .models import Classroom, Quiz
import unittest
from unittest import TextTestRunner


def create_classroom(request):
    if not request.user.is_authenticated():
        return render(request, 'grading_code/login.html')
    else:
        form = ClassroomForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.user = request.user
            classroom.save()
            return render(request, 'grading_code/detail.html', {'classroom': classroom})
        context = {
            "form": form,
        }
        return render(request, 'grading_code/create_classroom.html', context)


def create_quiz(request, classroom_id):
    form = QuizForm(request.POST or None, request.FILES or None)
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    if form.is_valid():
        classroom_quizs = classroom.quiz_set.all()
        for s in classroom_quizs:
            if s.quiz_title == form.cleaned_data.get("quiz_title"):
                context = {
                    'classroom': classroom,
                    'form': form,
                    'error_message': 'You already added that quiz',
                }
                return render(request, 'grading_code/create_quiz.html', context)
        quiz = form.save(commit=False)
        quiz.classroom = classroom
        quiz.save()
        return render(request, 'grading_code/detail.html', {'classroom': classroom})
    context = {
        'classroom': classroom,
        'form': form,
    }
    return render(request, 'grading_code/create_quiz.html', context)


def delete_classroom(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    classroom.delete()
    return render(request, 'grading_code/index.html', {'classroom': classroom})


def delete_quiz(request, classroom_id, quiz_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz.delete()
    return render(request, 'grading_code/detail.html', {'classroom': classroom})


def detail(request, classroom_id):
    if not request.user.is_authenticated():
        return render(request, 'grading_code/login.html')
    else:
        user = request.user
        classroom = get_object_or_404(Classroom, pk=classroom_id)
        return render(request, 'grading_code/detail.html', {'classroom': classroom, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'grading_code/login.html')
    else:
        classrooms = Classroom.objects.filter(user=request.user)
        quiz_results = Quiz.objects.all()
        query = request.GET.get("q")
        if query:
            classrooms = classrooms.filter(
                Q(name__icontains=query) |
                Q(year__icontains=query)
            ).distinct()
            quiz_results = quiz_results.filter(
                Q(quiz_title__icontains=query)
            ).distinct()
            return render(request, 'grading_code/index.html', {
                'classrooms': classrooms,
                'quizs': quiz_results,
            })
        else:
            return render(request, 'grading_code/index.html', {'classrooms': classrooms})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'grading_code/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                classrooms = Classroom.objects.filter(user=request.user)
                return render(request, 'grading_code/index.html', {'classrooms': classrooms})
            else:
                return render(request, 'grading_code/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'grading_code/login.html', {'error_message': 'Invalid login'})
    return render(request, 'grading_code/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                classrooms = Classroom.objects.filter(user=request.user)
                return render(request, 'grading_code/index.html', {'classrooms': classrooms})
    context = {
        "form": form,
    }
    return render(request, 'grading_code/register.html', context)


def quizs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'grading_code/login.html')
    else:
        try:
            quiz_ids = []
            for classroom in Classroom.objects.filter(user=request.user):
                for quiz in classroom.quiz_set.all():
                    quiz_ids.append(quiz.pk)
            users_quizs = Quiz.objects.filter(pk__in=quiz_ids)
            if filter_by == 'favorites':
                users_quizs = users_quizs.filter(is_favorite=True)
        except Classroom.DoesNotExist:
            users_quizs = []
        return render(request, 'grading_code/quizs.html', {
            'quiz_list': users_quizs,
            'filter_by': filter_by,
        })


def grading(request, classroom_id, quiz_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    return render(request, 'grading_code/grading.html', {'quiz': quiz, 'classroom': classroom})


def grade(request, classroom_id, quiz_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == "POST":
        code = request.POST['code']
        code = code.lower()
    class MyTestCase(unittest.TestCase):
        def test_text(self):
            text = code
            self.assertEquals(text, "print('hello world')")
        def test_text_two(self):
            text = code
            self.assertEqual(text, 'print("hello world")')

    test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    test_result = TextTestRunner().run(test_suite)
    x = len(test_result.failures)
    if x == 1:
        result = "PASS"
    else:
        result = "FAIL"
    return render(request, 'grading_code/grading.html', {
        'quiz': quiz, 'classroom': classroom, 'display': result, 'code': code,
    })
