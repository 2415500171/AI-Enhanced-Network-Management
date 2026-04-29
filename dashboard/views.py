from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from ml_engine.services import compute_dashboard_payload, load_dataframe, simulate_live_reading


@login_required
def dashboard_home(request):
    df = load_dataframe()
    payload = compute_dashboard_payload(df)
    return render(request, "dashboard/dashboard.html", payload)


@login_required
def live_data_api(request):
    data = simulate_live_reading()
    return JsonResponse(data)