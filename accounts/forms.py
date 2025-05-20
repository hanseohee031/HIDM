from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Announcement  # 맨 위 import 추가 필요


### 1. 회원가입용 SignupForm
class SignupForm(UserCreationForm):
    student_id = forms.CharField(label="Student ID Number")
    nickname = forms.CharField(label="Nickname")
    gender = forms.ChoiceField(
        label="Gender",
        choices=UserProfile.GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    native_language = forms.ChoiceField(
        label="Native Language",
        choices=UserProfile.NATIVE_LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['student_id', 'nickname', 'gender', 'native_language',  'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['student_id']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                nickname=self.cleaned_data['nickname'],
                gender=self.cleaned_data['gender'],
                native_language=self.cleaned_data['native_language'],
            )
        return user

### 2. 기본 프로필 작성/수정용
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'nickname',
            'gender',
            'native_language',
            'bio',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'native_language': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        qs = UserProfile.objects.filter(nickname=nickname)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This nickname is already in use. Please choose another one.")
        return nickname

### 3. 고급 프로필 입력용 (Advanced Profile)
class AdvancedProfileForm(forms.ModelForm):
    nationality = forms.ChoiceField(
        label="Nationality",
        choices=UserProfile.NATIONALITY_CHOICES,   # <- models.py에 NATIONALITY_CHOICES가 정의되어야 함
        required=False,
        widget=forms.Select(attrs={'class': 'select2'})
    )
    class Meta:
        model = UserProfile
        fields = [
            'born_year', 'show_born_year',
            'nationality', 'show_nationality',
            'major', 'show_major',
            'instagram_id', 'show_instagram',
            'personality', 'show_personality',
            'bio', 'show_bio',
        ]
        widgets = {
            'nationality': forms.Select(attrs={'class': 'form-select'}),
            # 여기에 더 필요한 필드 widget 옵션 추가 가능
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
