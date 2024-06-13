from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserFootprintForm
from .models import UserFootprint
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def about(request):
    return render(request, 'ecofootprint/about.html')


@login_required
def calculate_footprint(request):
    if request.method == 'POST':
        form = UserFootprintForm(request.POST)
        if form.is_valid():
            footprint = form.save(commit=False)
            footprint.user = request.user
            footprint.save()
            return redirect('result')
    else:
        form = UserFootprintForm()
    return render(request, 'ecofootprint/calculate.html', {'form': form})


@login_required
def result(request):
    latest_entry = UserFootprint.objects.filter(user=request.user).latest('date_created')
    total_footprint = (
            latest_entry.energy_consumption * 0.233 +
            latest_entry.meat_consumption * 7.2 +
            latest_entry.travel_distance * 0.21 +
            latest_entry.waste_production * 0.5
    )
    # return render(request, 'ecofootprint/result.html', {'entry': latest_entry, 'total_footprint': total_footprint})
    message = None
    message_color = None
    if total_footprint < 100:
        message = "Great job! Your carbon footprint is below the threshold."
        message_color = "green"
    else:
        message = "Your carbon footprint is above the threshold. Please consider ways to reduce it!"
        message_color = "red"
    return render(request, 'ecofootprint/result.html',
                  {'entry': latest_entry, 'total_footprint': total_footprint, 'message': message,
                   'message_color': message_color})


def account(request):
    user = request.user
    return render(request, 'ecofootprint/user.html', {'user': user})
