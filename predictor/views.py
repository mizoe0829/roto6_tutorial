from django.shortcuts import render
from .logic import generate_predictions


def top(request):
    predictions = generate_predictions()
    return render(request, "predictor/top.html", {"predictions": predictions})