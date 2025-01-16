from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job
from markdown import markdown
from weasyprint import HTML

from .models import Enrollment


@job
def deliver_certificate(base_url, student):
    enrollments = Enrollment.objects.filter(student=student)
    rendered = render_to_string(
        'subjects/certificates/certificates.html', {'student': student, 'enrollments': enrollments}
    )
    output_path = settings.CERTIFICATE_DIR / f'{student.username}_grade_certificate.pdf'
    HTML(string=rendered, base_url=base_url).write_pdf(output_path)
    rendered = render_to_string('subjects/certificates/email.md', {'student': student})
    email = EmailMessage(
        subject='Tu certificado de notas de lumino',
        body=markdown(rendered),
        from_email=None,
        to=[student.email],
    )
    email.content_subtype = 'html'
    email.attach_file(str(output_path))
    email.send()
