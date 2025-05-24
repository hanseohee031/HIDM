# accounts/management/commands/seed_fake_profiles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, Category
from faker import Faker
import random

# 국가코드 → Faker 로케일 매핑
FOREIGN_LOCALES = {
    'US': 'en_US', 'GB': 'en_GB', 'CA': 'en_CA', 'AU': 'en_AU',
    'FR': 'fr_FR', 'DE': 'de_DE', 'ES': 'es_ES', 'IT': 'it_IT',
    'RU': 'ru_RU', 'BR': 'pt_BR', 'CN': 'zh_CN', 'JP': 'ja_JP',
    'IN': 'en_IN', 'NO': 'no_NO',
}

# 국적 → 기본 모국어 코드 매핑
NAT_TO_LANG = {
    'KR': 'ko',
    **{nat: locale.split('_')[0] for nat, locale in FOREIGN_LOCALES.items()}
}

# 전체 언어코드 목록 (예외 케이스용)
ALL_LANG_CODES = list(set(NAT_TO_LANG.values()))

# 관심사 카테고리 리스트
INTEREST_CATEGORY_NAMES = [
    'Health/Fitness/Wellness',
    'Food/Cooking/Cafe',
    'Travel/Outdoor/Leisure',
    'Pets',
    'School/Academics',
    'Daily Life/Shopping/Home Life',
    'Entertainment/Hobbies',
    'Sports/Leisure',
    'Fashion/Beauty',
    'Relationships/Dating',
    'Self-Development/Career',
    'Society/Current Issues/Politics',
    'Digital/Tech/Development',
    'Arts/Creation/DIY',
    'Music/Instruments',
    'Reading/Writing',
]

# 예외 확률: 4%
EXCEPTION_RATE = 0.04

# 전공 리스트 확장
MAJORS = [
    'Computer Science', 'Business Administration', 'Psychology', 'Economics',
    'Software Engineering', 'International Relations', 'Literature', 'Electrical Engineering',
    'Mechanical Engineering', 'Civil Engineering', 'Chemical Engineering', 'Biology',
    'Chemistry', 'Physics', 'Environmental Science', 'Architecture', 'Law',
    'Medicine', 'Nursing', 'Art & Design', 'Music', 'Film & Media Studies',
    'Education', 'Statistics', 'Data Science', 'Philosophy', 'Sociology', 'Anthropology'
]

class Command(BaseCommand):
    help = 'Create fake profiles: 500 Koreans, 300 foreigners, with interests'

    def add_arguments(self, parser):
        parser.add_argument('--kor', type=int, default=500, help='Number of Korean profiles')
        parser.add_argument('--for', dest='forn', type=int, default=300, help='Number of foreign profiles')
        parser.add_argument('--pw', type=str, default='Test@1234', help='Raw password for all users')

    def handle(self, *args, **options):
        num_kor = options['kor']
        num_for = options['forn']
        raw_pw  = options['pw']
        # 지정한 관심사 카테고리에서만 선택
        cats = list(Category.objects.filter(name__in=INTEREST_CATEGORY_NAMES))

        # Faker 인스턴스 세팅
        faker_kr = Faker('ko_KR')
        faker_kr.unique.clear()
        faker_en = Faker('en_US')
        faker_en.unique.clear()
        for loc in FOREIGN_LOCALES.values():
            Faker(loc).unique.clear()

        # 한국인 프로필 생성
        for _ in range(num_kor):
            sid = str(random.randint(20210000, 20249999))
            while User.objects.filter(username=sid).exists():
                sid = str(random.randint(20210000, 20249999))

            user = User.objects.create_user(username=sid, password=raw_pw)
            bio_text = faker_en.sentence(nb_words=10)
            profile = UserProfile.objects.create(
                user=user,
                nickname=faker_kr.unique.user_name(),
                gender=random.choice([c[0] for c in UserProfile.GENDER_CHOICES]),
                native_language=NAT_TO_LANG['KR'],
                major=random.choice(MAJORS),
                born_year=random.randint(1995, 2005),
                nationality='KR',
                personality=random.choice(['INTJ','ENTP','INFJ','ENFP','ISTJ','ISFJ','ESTP','ESFP']),
                bio=bio_text,
            )
            profile.favorite_categories.set(random.sample(cats, 5))
            profile.save()

        # 외국인 프로필 생성
        for _ in range(num_for):
            nat    = random.choice(list(FOREIGN_LOCALES.keys()))
            locale = FOREIGN_LOCALES[nat]
            fake   = Faker(locale)

            sid = str(random.randint(20250000, 20259999))
            while User.objects.filter(username=sid).exists():
                sid = str(random.randint(20250000, 20259999))

            user = User.objects.create_user(username=sid, password=raw_pw)
            if random.random() < EXCEPTION_RATE:
                possible = [lang for lang in ALL_LANG_CODES if lang != NAT_TO_LANG[nat]]
                native_lang = random.choice(possible)
            else:
                native_lang = NAT_TO_LANG[nat]

            bio_text = faker_en.sentence(nb_words=10)
            profile = UserProfile.objects.create(
                user=user,
                nickname=fake.unique.user_name(),
                gender=random.choice([c[0] for c in UserProfile.GENDER_CHOICES]),
                native_language=native_lang,
                major=random.choice(MAJORS),
                born_year=random.randint(1990, 2005),
                nationality=nat,
                personality=random.choice(['INTJ','ENTP','INFJ','ENFP','ISTJ','ISFJ','ESTP','ESFP']),
                bio=bio_text,
            )
            profile.favorite_categories.set(random.sample(cats, 5))
            profile.save()

        self.stdout.write(self.style.SUCCESS(
            f"✅ Created {num_kor} Korean + {num_for} foreign fake profiles (password='{raw_pw}')"
        ))
