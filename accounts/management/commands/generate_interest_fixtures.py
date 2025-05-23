import json
from collections import OrderedDict
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "category_keywords.json을 읽어서 interest_pool.json용 fixture 형식으로 변환합니다."

    def handle(self, *args, **options):
        raw = json.load(
            open("accounts/fixtures/category_keywords.json", encoding="utf-8"),
            object_pairs_hook=OrderedDict
        )

        out = []
        cat_pk = 1
        item_pk = 1

        for i, (cat_name, items) in enumerate(raw.items(), start=1):
            out.append({
                "model": "accounts.interestcategory",
                "pk": cat_pk,
                "fields": {"name": cat_name, "order": i}
            })
            for itm in items:
                out.append({
                    "model": "accounts.interest",
                    "pk": item_pk,
                    "fields": {"category": cat_pk, "name": itm}
                })
                item_pk += 1
            cat_pk += 1

        with open("accounts/fixtures/interest_pool.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            "✅ accounts/fixtures/interest_pool.json 생성 완료"
        ))
