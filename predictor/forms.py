from django import forms


class DrawForm(forms.Form):
    draw_number = forms.IntegerField(label="回号")
    draw_date = forms.DateField(label="抽選日", widget=forms.DateInput(attrs={"type": "date"}))
    number_1 = forms.IntegerField(label="数字1", min_value=1, max_value=43)
    number_2 = forms.IntegerField(label="数字2", min_value=1, max_value=43)
    number_3 = forms.IntegerField(label="数字3", min_value=1, max_value=43)
    number_4 = forms.IntegerField(label="数字4", min_value=1, max_value=43)
    number_5 = forms.IntegerField(label="数字5", min_value=1, max_value=43)
    number_6 = forms.IntegerField(label="数字6", min_value=1, max_value=43)
    bonus_number = forms.IntegerField(label="ボーナス数字", min_value=1, max_value=43)

    def to_draw_dict(self) -> dict:
        data = self.cleaned_data
        return {
            "draw_number": data["draw_number"],
            "draw_date": data["draw_date"].isoformat(),
            "numbers": sorted([data[f"number_{i}"] for i in range(1, 7)]),
            "bonus_number": data["bonus_number"],
        }