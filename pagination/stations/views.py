from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from django.conf import settings


CONTENT = [str(i) for i in range(10000)]


def index(request):  # вот эта функция перенаправляет с главной страницы на bus_stations?
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    f = settings.BUS_STATION_CSV
    with open(f, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        stations = [i for i in reader]

        # почему-то вот здесь класс OrderedDict из collections, хотя в документации сказано с версии 3.8 просто dict
        # print(type(stations[5]), station[5])

        page = int(request.GET.get('page', 1))
        elements_per_page = 10
        paginator = Paginator(stations, elements_per_page)
        page_ = paginator.get_page(page)
        content = page_.object_list

        context = {
            'bus_stations': content,
            'page': page_,
        }
        return render(request, 'stations/index.html', context)


def pagi_view(request):
    try:
        page = int(request.GET.get('page', 1))  # вот здесь 0, это если не будет page  в запросе
    except ValueError:  # а вот это если не ИНТ введут
        page = 1
    print(page)
    elements_per_page = 10
    # content = CONTENT[page * elements_per_page: page * elements_per_page + elements_per_page]

    paginator = Paginator(CONTENT, elements_per_page)
    page_ = paginator.get_page(page)
    content = page_.object_list
    return HttpResponse('<br>'.join(content))