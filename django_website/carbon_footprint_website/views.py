from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserFootprintForm
from .models import UserFootprint


def calculate_footprint(request):
    if request.method == 'POST':
        form = UserFootprintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = UserFootprintForm()
    return render(request, 'ecofootprint/calculate.html', {'form': form})


def result(request):
    latest_entry = UserFootprint.objects.latest('date_created')
    total_footprint = (
            latest_entry.energy_consumption * 0.233 +
            latest_entry.meat_consumption * 7.2 +
            latest_entry.travel_distance * 0.21 +
            latest_entry.waste_production * 0.5
    )
    return render(request, 'ecofootprint/result.html', {'entry': latest_entry, 'total_footprint': total_footprint})


def index(request):
    context = {}
    template = loader.get_template('ecofootprint/index.html')
    return HttpResponse(template.render(context, request))


def login(request):
    return HttpResponse("TODO")
