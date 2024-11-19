import logging

from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacher, IsAdmin

logger = logging.getLogger('myapp')

class AttendanceListView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()


class AttendanceMarkingView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        attendance = serializer.save()
        logger.info(f'Attendance marked for student: {attendance.student.username} in course: {attendance.course.name} on {attendance.date}')