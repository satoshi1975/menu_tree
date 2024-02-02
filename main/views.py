
from django.shortcuts import render


def any_section(request,section_name):
    return render(request, 'for_any.html', {'section_name':section_name})


    