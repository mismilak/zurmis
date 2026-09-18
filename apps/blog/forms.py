from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ["name", "email", "content"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "نام شما", "class": "form-control"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "ایمیل (نمایش داده نمی‌شود)", "class": "form-control"}
            ),
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "دیدگاه خود را بنویسید…", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = False

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("خطا در ارسال فرم.")
        return ""
