from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from django_q.tasks import async_task
from django.core.mail import send_mail

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@api_view(['POST'])
def upload_file(request):
    if 'file' not in request.FILES:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    for index, row in data.iterrows():
        Student.objects.create(
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            department=row['department'],
            student_id=row['student_id'],
        )

    return Response(status=status.HTTP_201_CREATED)


def process_file(file):
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)

    for index, row in data.iterrows():
        Student.objects.create(
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            department=row['department'],
            student_id=row['student_id'],
        )

    send_mail(
        'Data Processing Complete',
        'Your data processing is complete.',
        'practicejava68@gmail.com',
        ['admin@gmail.com.com'],
        fail_silently=False,
    )

@api_view(['POST'])
def upload_file(request):
    if 'file' not in request.FILES:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    async_task(process_file, file)
    return Response(status=status.HTTP_201_CREATED)
