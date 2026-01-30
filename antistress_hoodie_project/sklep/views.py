from django.shortcuts import render, redirect
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .models import Person, Position
from .serializers import PersonSerializer, PositionSerializer
from .forms import PersonForm, PositionForm
from django.http import Http404, HttpResponse
from .forms import PersonForm


@api_view(['GET', 'POST'])
def person_list(request):
    if request.method == 'GET':
        surname_query = request.query_params.get('nazwisko', None)
        
        if surname_query:
            people = Person.objects.filter(surname__icontains=surname_query)
        else:
            people = Person.objects.all()

        serializer = PersonSerializer(people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def person_detail(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def position_list(request):
    if request.method == 'GET':
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def position_detail(request, pk):
    try:
        position = Position.objects.get(pk=pk)
    except Position.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PositionSerializer(position)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PositionSerializer(position, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        position.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def person_list_html(request):
    people = Person.objects.all()
    return render(request, 'sklep/person/list.html', {'people': people})

def person_detail_html(request, id):
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        raise Http404("Person object with the specified ID does not exist")
    
    if request.method == "GET":
        return render(request, "sklep/person/detail.html", {'person': person})
    
    if request.method == "POST":
        person.delete()
        return redirect('osoba-list') 

def person_create_html(request):
    positions = Position.objects.all()
    if request.method == "GET":
        return render(request, "sklep/person/create.html", {'positions': positions})
    elif request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        gender = request.POST.get('gender')
        position_id = request.POST.get('position_id')

        if name and surname and gender and position_id:
            try:
                position_obj = Position.objects.get(id=position_id)
            except Position.DoesNotExist:
                error = "Chosen position does not exist."
                return render(request, "sklep/person/create.html", {'error': error, 'positions': positions})

            Person.objects.create(
                name=name,
                surname=surname,
                gender=gender,
                position=position_obj
            )
            return redirect('people-list')
        else:
            error = "All fields are required"
            return render(request, "sklep/person/create.html", {'error': error, 'positions': positions})
        
def person_create_django_form(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('osoba-list')  
    else:
        form = PersonForm()

    return render(request,
                  "sklep/person/create_django.html",
                  {'form': form})



def position_list_html(request):
    positions = Position.objects.all()
    return render(request, 'sklep/position/list.html', {'positions': positions})

def position_detail_html(request, id):
    position = Position.objects.get(id=id)
    return render(request, 'sklep/position/detail.html', {'position': position})

def position_create_django_form(request):
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('position-list')  
    else:
        form = PositionForm()

    return render(request,
                  "sklep/position/create_django.html",
                  {'form': form})