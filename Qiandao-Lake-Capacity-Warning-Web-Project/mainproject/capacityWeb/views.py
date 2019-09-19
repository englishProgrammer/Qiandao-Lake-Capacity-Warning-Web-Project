from django.shortcuts import render


# Create your views here.

def index(request):
    """
    跳转至 index.html
    """
    return render(request, 'index.html')


def test(request):
    return render(request, 'test.html')
