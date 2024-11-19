import logging
from rest_framework import generics, permissions
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsTeacher, IsAdmin

logger = logging.getLogger('myapp')


class GradeListView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()


class GradeUpdateView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        grade = serializer.save()
        logger.info(f'Grade updated for student: {grade.student.username} in course: {grade.course.name} by teacher: {grade.teacher.username} on {grade.date}')