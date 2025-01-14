from subjects.models import Enrollment


def get_all_subjects(request) -> dict:
    if request.user.is_authenticated:
        try:
            user_role = request.user.profile.get_role()
            match user_role:
                case 'Student':
                    subjects = request.user.enrolled_subjects.all()
                case 'Teacher':
                    subjects = request.user.subjects.all()
            return {'get_all_subjects': subjects}
        except Enrollment.DoesNotExist:
            return {}
    else:
        return {}
