from django.shortcuts import render
from django.http import JsonResponse    
from students.models import Student
from .serializers import EmployeeSerializer, StudentSerializer
from rest_framework.response import Response
from rest_framework import status #give status code 
from rest_framework.decorators import api_view    
from rest_framework.views import APIView
from employees.models import Employee
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from blogs.models import Blog,Comment   
from blogs.serializers import BlogSerializer,CommentSerializer
from .paginations import CustomPageNumberPagination, CustomLimitOffsetPagination
from employees.filters import EmployeeFilter
from rest_framework import filters
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import filters

# --- CSRF Token Error Fix ---
# The following custom authentication class disables CSRF protection for API endpoints.
# This is necessary because Django's default CSRF protection blocks POST, PUT, DELETE requests from clients like Postman or JavaScript apps.
# For APIs, CSRF is not required, so we skip the check here.
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Skip CSRF check
from django .http import HttpResponse
from rest_framework import mixins, generics
# Create your views here.
@api_view(['GET', 'POST'])
def studentsView(request):
    if request.method == 'GET':
        #get all the data from the student table    
        students=Student.objects.all()
        #serialize the data 
        serializer=StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        #get the data from the request 
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#@api_view(['GET', 'PUT', 'DELETE'])   
@api_view(['GET', 'PUT', 'DELETE'])
def studentDetailView(request, pk):
    try:
        student=Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer=StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer=StudentSerializer(student, data=request.data) #updating the existing data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #decide automatically the request to be processd
    #this is a classs based view and it is used for more complex operations used  for large applications
    #we creating class based view for employees
    #class based view doesn't support decorators
    """
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Skip CSRF check

#@method_decorator(csrf_exempt, name='dispatch')
class Employees(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    def get(self, request):
        employees=Employee.objects.all()
        serializer=EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #put and delete methods can be added here
    #to perform operations on single employee record
    #we can create another class based view for that
    #EmployeesDetail(APIView)
class EmployeeDetail(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    def get_object(self, pk): #to get the object based on primary key FROM db
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None
    def get(self, request, pk):
        employee=self.get_object(pk)
        if employee is None:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk):
        employee=self.get_object(pk)
        if employee is None:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        employee=self.get_object(pk)
        if employee is None:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    mixins are reusable code class in oops that provide speifec functionality to the child class
    in DRF we have mixins for common operations like create, update, delete, list, retrieve
    we can use these mixins to create class based views with less code
    5 mixins are available in DRF
    CreateModelMixin--- support for creating a new object
    UpdateModelMixin--- support for updating an existing object using pk using update method
    DestroyModelMixin--- support for deleting an object using fnction   delete method destroy()
    ListModelMixin--- support for returning the list of objects
    RetrieveModelMixin--- support for returning a single object

    class Employees(mixins, generic.GenericAPIView):
    
    def get(self, request):
        return self.list(request) 

    
    generic.GenericAPIView--- provides the core functionality for class based views like authentication, permission, throttling, etc also responsible for taking incoming http request
    """

"""

                    #mixins
# --- CSRF Token Error Fix ---
# Set authentication_classes to use CsrfExemptSessionAuthentication for Employees API endpoint.
# This disables CSRF protection for GET and POST requests to /api/v1/employees/.
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)






# --- CSRF Token Error Fix ---
# Set authentication_classes to use CsrfExemptSessionAuthentication for EmployeeDetail API endpoint.
# This disables CSRF protection for GET, PUT, and DELETE requests to /api/v1/employees/<pk>/.
class EmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    def get(self, request, pk):
        return self.retrieve(request, pk=pk)
    def put(self, request, pk):
        return self.update(request, pk=pk)
    def delete(self, request, pk):
        return self.destroy(request, pk=pk)
    
        
        """
"""
# Generics
# generics are built on top of mixins and genericAPIView to provide more functionality with less code
# in generics we dont have to define get, put, delete methods
# we can directly call the mixin methods like retrieve, update, destroy
# prebuilt methods are available in generics
# listapi view for listing all the employees
# retrieveapi view for retrieving a single employee using pk  
# updateapi view for updating a single employee using pk
# destroyapi view for deleting a single employee using pk
# createapi view for creating a new employee
# combinations of mixins and generics can be used to create class based views with less code
# listcreateapiview for listing and creating employees
# retrieveupdateapiview for retrieving and updating a single employee using pk
# retrievedestroyapiview for retrieving and deleting a single employee using pk


# --- CSRF Token Error Fix ---
# Set authentication_classes to use CsrfExemptSessionAuthentication for Employees generic API endpoint.
# This disables CSRF protection for GET and POST requests to /api/v1/employees/.
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]



# --- CSRF Token Error Fix ---
# Set authentication_classes to use CsrfExemptSessionAuthentication for EmployeeDetail generic API endpoint.
# This disables CSRF protection for GET, PUT, PATCH, and DELETE requests to /api/v1/employees/<pk>/.
class EmployeeDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]



    #viewsets
    # ViewSets are used to combine the logic for a set of related views in a single class  operations of mixin and generics can be combined in a single class using viewsets
    #viewsets.viewset has list, create, retrieve, update, partial_update, destroy methods
    #viewsets.modelviewset has all the methods of viewset and also provides default implementations for create, retrieve, update, partial_update, destroy, list actions
    #we can use routers to automatically generate the urls for viewsets
    """

# class EmployeeViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Employee.objects.all()
#         serializer = EmployeeSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         try:
#             employee = Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             employee = Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         try:
#             employee = Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
class EmployeeViewSet(viewsets.ModelViewSet): # all the operations in a single class, both non pkey and pkey
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]   
    pagination_class = CustomPageNumberPagination  # Add pagination to the viewset
    #filterset_fields = ['designation']  # Enable filtering by designation and name
    filterset_class = EmployeeFilter  #for custom filter class case insensitive

    #nested serializers for one to many relationship
    #in student model we have a foreign key to the employee model 

class BlogsView(generics.ListCreateAPIView):
   
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['blog_title'] #search by title and content
    ordering_fields = ['id']  # Allow ordering by id and blog_title

class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

    #pagination
    #pagination is used to limit the number of records returned in a single response
    #to create a comment we need to provide the blog id in the request body
    #to create a comment we need to provide the blog id in the request body
    #pagenumber pagination--- we can specify the page number and the number of records per page in the request
    #takespage and page_size as parameters

    #limitoffset pagination--- we can specify the limit and offset in the request
    #takes limit and offset as parameters
    #2 types of pahgination are available in DRF
    #global pagination--- we can set the pagination for all the views in the settings.py file
    #custom pagination--- we can set the pagination for a specific view by adding the pagination_class



    #filtering
    #filtering is used to filter the records based on certain criteria
    #we can use django filter backend to filter the records
    #we need to install django-filter package to use django filter backend

    #filter usecases
    #filtering based on a single field
    #filtering based on multiple fields
    #searching based on a single field

    #filter employee by designation
    #filter employee by name
    #filter employee by id

#filters are case sensitive
#exact--- exact match
#so we use custom filter class to make it case insensitive


#searching
#searching is used to search the records based on a keyword 


#ordering#ordering is used to order the records based on a field
#we can use ordering filter backend