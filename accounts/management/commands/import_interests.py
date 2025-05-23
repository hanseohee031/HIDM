import json
from django.core.management.base import BaseCommand
from accounts.models import Interest

class Command(BaseCommand):
    help = "category_keywords.json을 읽어서 Interest 모델에 직접 저장합니다."

    def handle(self, *args, **options):
        path = "accounts/fixtures/category_keywords.json"
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        created, skipped = 0, 0
        for category, names in data.items():
            for name in names:
                # 중복 방지: 동일한 category+name이 없을 때만 생성
                obj, is_new = Interest.objects.get_or_create(
                    category=category,
                    name=name
                )
                if is_new:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Interests imported: {created} created, {skipped} skipped"
        ))
