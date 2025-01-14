from django_rq import job


@job
def deliver_certificate(base_url):
    pass
