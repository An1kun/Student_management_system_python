# students/views.py

from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsStudent, IsTeacher, IsAdmin
from rest_framework.permissions import IsAuthenticated

class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Only admin can list and create students

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsAdmin]  # Only admin can edit or delete
        else:
            self.permission_classes = [IsAuthenticated, IsStudent]  # Students can view their own details
        return super().get_permissions()
