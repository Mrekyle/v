from django.shortcuts import render

def handler404(request, excemption):
    """"
        Error 404 handling
    """

    template = 'errors/404.html'

    return render(request, template, status=404)

def handler500(request):
    """
        Error 500 handling
    """

    template = 'errors/500.html'

    return render(request, template, status=500)