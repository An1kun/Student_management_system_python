
from courses.serializers import EnrollmentSerializer
from grades.serializers import GradeSerializer
from attendance.serializers import AttendanceSerializer

class StudentDetailSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    grades = GradeSerializer(many=True, read_only=True)
    attendance_records = AttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'name', 'dob', 'registration_date', 'enrollments', 'grades', 'attendance_records']
