from django import template

register = template.Library()


@register.inclusion_tag('subjects/marks/student_label.html')
def student_label(formset, form_index):
    student = formset.forms[form_index].instance.student
    return dict(student=student)
