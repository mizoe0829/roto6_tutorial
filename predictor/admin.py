from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .forms import DrawForm
from .logic import append_draw
from .analytics import build_dataframe, number_frequency, bonus_frequency, summary_stats


@staff_member_required
def add_draw_view(request):
    if request.method == "POST":
        form = DrawForm(request.POST)
        if form.is_valid():
            append_draw(form.to_draw_dict())
            return redirect("admin:add_draw_done")
    else:
        form = DrawForm()
    return render(request, "admin/add_draw.html", {"form": form})


@staff_member_required
def add_draw_done_view(request):
    return render(request, "admin/add_draw_done.html")

@staff_member_required
def analytics_view(request):
    df = build_dataframe()

    if df.empty:
        context = {"has_data": False}
    else:
        freq = number_frequency(df)
        bonus_freq = bonus_frequency(df)
        stats = summary_stats(df)

        context = {
            "has_data": True,
            "stats": stats,
            "freq_labels": [int(x) for x in freq.index],
            "freq_values": [int(x) for x in freq.values],
            "bonus_labels": [int(x) for x in bonus_freq.index],
            "bonus_values": [int(x) for x in bonus_freq.values],
        }

    return render(request, "admin/analytics.html", context)


# 既存のadminのURLに追加する
_original_get_urls = admin.site.get_urls


def get_urls():
    custom_urls = [
        path("predictor/add-draw/", add_draw_view, name="add_draw"),
        path("predictor/add-draw/done/", add_draw_done_view, name="add_draw_done"),
        path("predictor/analytics/", analytics_view, name="analytics"),
    ]
    return custom_urls + _original_get_urls()


admin.site.get_urls = get_urls
admin.site.index_title = "ロト6予想サービス 管理"
admin.site.site_header = "ロト6 管理画面"