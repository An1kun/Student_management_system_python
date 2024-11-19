from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import generics
from .models import Student
from .serializers import StudentDetailSerializer, StudentSerializer
from users.permissions import IsStudent, IsAdmin

class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        student_id = kwargs['pk']
        cached_student = cache.get(f'student_profile_{student_id}')
        if cached_student is not None:
            return Response(cached_student)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(f'student_profile_{student_id}', response.data, timeout=60*15)  # Cache for 15 minutes
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        student_id = kwargs['pk']
        cache.delete(f'student_profile_{student_id}')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        student_id = kwargs['pk']
        cache.delete(f'student_profile_{student_id}')
        return response

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsStudent]
        return super().get_permissions()