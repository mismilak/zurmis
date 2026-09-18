"""فرم‌های بخش اصلی سایت."""
import re

from django import forms

from .models import ConsultationRequest, PracticeArea

PHONE_RE = re.compile(r"^(?:\+?98|0)?9\d{9}$|^0\d{9,10}$")
FA_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


class ConsultationForm(forms.ModelForm):
    # فیلد تله برای ربات‌ها (برای کاربر نمایش داده نمی‌شود)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ConsultationRequest
        fields = ["full_name", "phone", "email", "subject", "preferred_time", "message"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"placeholder": "نام و نام خانوادگی", "autocomplete": "name"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "۰۹۱۲۱۲۳۴۵۶۷", "inputmode": "tel", "autocomplete": "tel"}
            ),
            "email": forms.EmailInput(attrs={"placeholder": "ایمیل (اختیاری)", "autocomplete": "email"}),
            "preferred_time": forms.TextInput(attrs={"placeholder": "مثلاً عصرها بعد از ساعت ۱۶"}),
            "message": forms.Textarea(
                attrs={"rows": 4, "placeholder": "موضوع پرونده خود را به‌طور خلاصه بنویسید…"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = PracticeArea.objects.filter(is_active=True)
        self.fields["subject"].empty_label = "موضوع پرونده را انتخاب کنید"
        self.fields["email"].required = False
        self.fields["preferred_time"].required = False
        for name, field in self.fields.items():
            if name == "website":
                continue
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").translate(FA_DIGITS)
        phone = re.sub(r"[\s\-()]", "", phone)
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("شماره تماس معتبر نیست. نمونه صحیح: ۰۹۱۲۱۲۳۴۵۶۷")
        return phone

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("خطا در ارسال فرم.")
        return ""
