from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .forms import UserFootprintForm
from .models import UserFootprint, UserFootprintAggregation
from django.contrib.auth.forms import UserCreationForm
from scipy import stats



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
            footprint.energy_consumption_footprint = footprint.energy_consumption * 0.233
            footprint.meat_consumption_footprint = footprint.meat_consumption * 7.2
            footprint.travel_distance_footprint = footprint.travel_distance * 0.21
            footprint.waste_production_footprint = footprint.waste_production * 0.5
            footprint.total_footprint = (
                    footprint.energy_consumption_footprint +
                    footprint.meat_consumption_footprint +
                    footprint.travel_distance_footprint +
                    footprint.waste_production_footprint
            )
            footprint.save()
            return redirect('result')
    else:
        form = UserFootprintForm()
    return render(request, 'ecofootprint/calculate.html', {'form': form})


@login_required
def result(request):
    latest_entry = UserFootprint.objects.filter(user=request.user).latest('date_created')
    total_footprint = latest_entry.total_footprint
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
    user_data = UserFootprint.objects.filter(user=request.user).order_by('-date_created')[:5]
    try:
        data_agg = UserFootprintAggregation.objects
        user_data_agg = data_agg.filter(user=request.user)
        percentiles = calculate_percentiles(user_data_agg, data_agg)
    except Exception:
        user_data_agg = {}
        percentiles = {}
    return render(request, 'ecofootprint/user.html', {'user': user, 'user_data': user_data,
                                                      'user_data_agg': user_data_agg, 'percentiles': percentiles})


def calculate_percentiles(user_data_agg, data_agg):
    percentiles = {}

    user_item = user_data_agg.latest('week')
    overall_week_data = data_agg.filter(week=user_item.week)
    # Calculate percentiles for each value in user_week_data
    values = overall_week_data.values_list('mean_energy_consumption_footprint', flat=True)
    percentile_energy = stats.percentileofscore(values, user_item.mean_energy_consumption_footprint)
    percentiles["energy"] = percentile_energy
    values = overall_week_data.values_list('mean_meat_consumption_footprint', flat=True)
    percentile_meat = stats.percentileofscore(values, user_item.mean_meat_consumption_footprint)
    percentiles["meat"] = percentile_meat
    values = overall_week_data.values_list('mean_travel_distance_footprint', flat=True)
    percentile_travel = stats.percentileofscore(values, user_item.mean_travel_distance_footprint)
    percentiles["travel"] = percentile_travel
    values = overall_week_data.values_list('mean_waste_production_footprint', flat=True)
    percentile_waste = stats.percentileofscore(values, user_item.mean_waste_production_footprint)
    percentiles["waste"] = percentile_waste
    values = overall_week_data.values_list('mean_total_footprint', flat=True)
    percentile_total = stats.percentileofscore(values, user_item.mean_total_footprint)
    percentiles["total"] = percentile_total

    return percentiles


@method_decorator(csrf_exempt, name='dispatch')
class RunCommandView(View):
    def post(self, request, *args, **kwargs):
        try:
            call_command('aggregate_data')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)