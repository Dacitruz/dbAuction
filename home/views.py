from django.shortcuts import render


def index(request):
    data = {'title': 'Main Page'}
    return render(request, 'home/index.html', context=data)


def about(request):
    data = {'title': 'About'}
    return render(request, 'home/about.html', context=data)


def contacts(request):
    data = {'title': 'Contacts'}
    return render(request, 'home/contacts.html', context=data)
