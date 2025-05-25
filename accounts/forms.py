from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Category
from .models import Announcement  # 맨 위 import 추가 필요
from .models import Interest
from .models import ChatRequest

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


### 4. 관심사 선택용 폼 ###
class InterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all().order_by('category', 'name'),
        widget=forms.CheckboxSelectMultiple,
        label="Select Your Interests",
        required=True,
    )

    class Meta:
        model = UserProfile
        fields = ['interests']

    def clean_interests(self):
        interests = self.cleaned_data.get('interests')
        if not interests or interests.count() != 5:
            raise forms.ValidationError("Please select exactly 5 interests.")
        return interests




from .models import Topic  # add this import at the top

# ─── 5. 토픽 추가용 폼 ───
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['category', 'title']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a new topic…'
            }),
        }
        labels = {
            'category': 'Topic Category',
            'title': 'Topic Title',
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']


class CategorySelectionForm(forms.ModelForm):
    favorite_categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="관심 카테고리 (정확히 5개 선택)"
    )

    class Meta:
        model = UserProfile
        fields = ['favorite_categories']

    def clean_favorite_categories(self):
        cats = self.cleaned_data.get('favorite_categories')
        count = cats.count() if cats is not None else 0
        if count != 5:
            raise forms.ValidationError("정확히 5개를 선택해야 합니다.")
        return cats


class ChatRequestForm(forms.ModelForm):
    class Meta:
        model = ChatRequest
        fields = ['slot1', 'slot2', 'slot3']
        widgets = {
            'slot1': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'slot2': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'slot3': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }
        labels = {
            'slot1': 'Option 1',
            'slot2': 'Option 2',
            'slot3': 'Option 3',
        }

    def clean(self):
        cleaned_data = super().clean()
        s1 = cleaned_data.get('slot1')
        s2 = cleaned_data.get('slot2')
        s3 = cleaned_data.get('slot3')

        # Ensure all three are provided
        if not (s1 and s2 and s3):
            raise forms.ValidationError(
                "Please select three time slots."
            )

        # Prevent duplicates
        if len({s1, s2, s3}) < 3:
            raise forms.ValidationError(
                "Please choose three distinct time slots."
            )

        return cleaned_data
