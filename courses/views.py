import logging
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import generics

from assignment2.users import permissions
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permissions import IsTeacher, IsAdmin

logger = logging.getLogger('myapp')


class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        cached_courses = cache.get('courses_list')
        if cached_courses is not None:
            return Response(cached_courses)

        response = super().list(request, *args, **kwargs)
        cache.set('courses_list', response.data, timeout=60*15)  # Cache for 15 minutes
        return response

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete('courses_list')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete('courses_list')
        return response

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class EnrollmentListView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdmin]

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdmin]


class CourseEnrollmentView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        enrollment = serializer.save()
        logger.info(f'Student enrolled: {enrollment.student.username} in course: {enrollment.course.name}')
