from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def home(request):
    return HttpResponse("HELLO   W")
    # return render(request,'templates/home.html')

    # return HttpResponse('home.html')


# Create your views here.


def tasks(request):
    tasks = Task.objects.all()
    return render(request, "tasks.html", {"tasks": tasks})


@api_view(["GET", "POST"])
def tasks(request, format=None):
    print("🐍 ",request.query_params)
    
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def task(request, id, format=None):
    try:
        task = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        return Response({"message": "Task Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        task.delete()
        return Response({"message": "Task Deleted"}, status=status.HTTP_204_NO_CONTENT)
