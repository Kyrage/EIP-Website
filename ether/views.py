from django.http.response import HttpResponse
from django.shortcuts import render

def handler401(request):
    """Error management 401 unauthorized\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Http response with html page that displays error 401 without data
    """
    context = {}
    return render(request, 'errors/401.html', context)

def handler404(request, exception):
    """Error management 404 page not found\n\n
    :param [request]: Receives an HttpRequest
    :param [exception]: Cause of the error returned by django
    :type [request]: HttpRequest
    :type [exception]: string
    :return: Http response with html page that displays error 404 without data
    """
    context = {}
    return render(request, 'errors/404.html', context)

def handler500(request):
    """Error management 500 internal server error\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Http response with html page that displays error 500 without data
    """
    context = {}
    return render(request, 'errors/500.html', context)

def home(request):
    context = {}
    return render(request, 'index.html', context)
