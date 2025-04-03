from django.shortcuts import render

# Create your views here.

def index_view(request):

    ctx = {

    }

    return render(request, 'main/index.html', ctx)


def custom_404(request, exception):
    return render(request, '404.html', status=404)