from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job
from markdown import markdown
from weasyprint import HTML


@job
def deliver_certificate(base_url, student):
    rendered = render_to_string('subjects/certificates/certificates.html')
    output_path = settings.CERTIFICATE_DIR / f'{student.username}_grade_certificate.pdf'
    HTML(string=rendered, base_url=base_url).write_pdf(output_path)
    rendered = render_to_string('subjects/certificates/email.md')
    email = EmailMessage(subject='A', body=markdown(rendered), from_email=None, to=[student.email])
    email.content_subtype = 'html'
    email.attach_file(str(output_path))
    email.send()
