from django.db import models
from django.contrib.auth.models import User


# ─── 1) 새 모델 추가: Interest ───
class Interest(models.Model):
    CATEGORY_CHOICES = [
        ('Hobbies', 'Hobbies & Leisure'),
        ('Travel', 'Travel & Adventure'),
        ('Food', 'Food & Drink'),
        ('Music', 'Music'),
        ('Sports', 'Sports'),
        ('Entertainment', 'Entertainment & Media'),
        ('Beauty', 'Beauty & Fashion'),
        ('Science', 'Science & IT'),
        ('Social', 'Social & Community'),
        ('Creative', 'Creative & Arts'),
        ('Pets', 'Pets & Animals'),
        ('Language', 'Languages'),
        ('Auto', 'Automotive & Motorsports'),
        ('Culture', 'Arts & Culture'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Interest Category'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Interest Name'
    )

    class Meta:
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'






class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='topics'
    )
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    upvotes = models.ManyToManyField(
        User,
        related_name='upvoted_topics',
        blank=True
    )
    downvotes = models.ManyToManyField(
        User,
        related_name='downvoted_topics',
        blank=True
    )

    @property
    def score(self):
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # One-to-one link with Django User (username stores Student ID Number)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- Basic Profile (always public) ---
    nickname = models.CharField(
        max_length=30,
        blank=False,
        verbose_name='Nickname'
    )

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Gender'
    )

    NATIVE_LANGUAGE_CHOICES = [
        ('ab', 'Abkhaz'), ('aa', 'Afar'), ('af', 'Afrikaans'), ('ak', 'Akan'),
        ('sq', 'Albanian'), ('am', 'Amharic'), ('ar', 'Arabic'), ('an', 'Aragonese'),
        ('hy', 'Armenian'), ('as', 'Assamese'), ('av', 'Avaric'), ('ae', 'Avestan'),
        ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('bm', 'Bambara'), ('ba', 'Bashkir'),
        ('eu', 'Basque'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('bh', 'Bihari'),
        ('bi', 'Bislama'), ('bs', 'Bosnian'), ('br', 'Breton'), ('bg', 'Bulgarian'),
        ('my', 'Burmese'), ('ca', 'Catalan; Valencian'), ('ch', 'Chamorro'),
        ('ce', 'Chechen'), ('ny', 'Chichewa; Chewa; Nyanja'), ('zh', 'Chinese'),
        ('cv', 'Chuvash'), ('kw', 'Cornish'), ('co', 'Corsican'), ('cr', 'Cree'),
        ('hr', 'Croatian'), ('cs', 'Czech'), ('da', 'Danish'),
        ('dv', 'Divehi; Dhivehi; Maldivian;'), ('nl', 'Dutch'), ('dz', 'Dzongkha'),
        ('en', 'English'), ('eo', 'Esperanto'), ('et', 'Estonian'), ('ee', 'Ewe'),
        ('fo', 'Faroese'), ('fj', 'Fijian'), ('fi', 'Finnish'), ('fr', 'French'),
        ('ff', 'Fula; Fulah; Pulaar; Pular'), ('gl', 'Galician'), ('ka', 'Georgian'),
        ('de', 'German'), ('el', 'Greek, Modern'), ('gn', 'Guaraní'), ('gu', 'Gujarati'),
        ('ht', 'Haitian; Haitian Creole'), ('ha', 'Hausa'), ('he', 'Hebrew (modern)'),
        ('hz', 'Herero'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hu', 'Hungarian'),
        ('ia', 'Interlingua'), ('id', 'Indonesian'), ('ie', 'Interlingue'), ('ga', 'Irish'),
        ('ig', 'Igbo'), ('ik', 'Inupiaq'), ('io', 'Ido'), ('is', 'Icelandic'),
        ('it', 'Italian'), ('iu', 'Inuktitut'), ('ja', 'Japanese'), ('jv', 'Javanese'),
        ('kl', 'Kalaallisut, Greenlandic'), ('kn', 'Kannada'), ('kr', 'Kanuri'),
        ('ks', 'Kashmiri'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('ki', 'Kikuyu, Gikuyu'),
        ('rw', 'Kinyarwanda'), ('ky', 'Kirghiz, Kyrgyz'), ('kv', 'Komi'), ('kg', 'Kongo'),
        ('ko', 'Korean'), ('ku', 'Kurdish'), ('kj', 'Kwanyama, Kuanyama'), ('la', 'Latin'),
        ('lb', 'Luxembourgish, Letzeburgesch'), ('lg', 'Luganda'),
        ('li', 'Limburgish, Limburgan, Limburger'), ('ln', 'Lingala'), ('lo', 'Lao'),
        ('lt', 'Lithuanian'), ('lu', 'Luba-Katanga'), ('lv', 'Latvian'), ('gv', 'Manx'),
        ('mk', 'Macedonian'), ('mg', 'Malagasy'), ('ms', 'Malay'), ('ml', 'Malayalam'),
        ('mt', 'Maltese'), ('mi', 'Māori'), ('mr', 'Marathi (Marāṭhī)'),
        ('mh', 'Marshallese'), ('mn', 'Mongolian'), ('na', 'Nauru'), ('nv', 'Navajo, Navaho'),
        ('nb', 'Norwegian Bokmål'), ('nd', 'North Ndebele'), ('ne', 'Nepali'), ('ng', 'Ndonga'),
        ('nn', 'Norwegian Nynorsk'), ('no', 'Norwegian'), ('ii', 'Nuosu'), ('nr', 'South Ndebele'),
        ('oc', 'Occitan'), ('oj', 'Ojibwe, Ojibwa'),
        ('cu', 'Old Church Slavonic, Church Slavonic, Old Bulgarian'), ('om', 'Oromo'),
        ('or', 'Oriya'), ('os', 'Ossetian, Ossetic'), ('pa', 'Panjabi, Punjabi'),
        ('pi', 'Pāli'), ('fa', 'Persian'), ('pl', 'Polish'), ('ps', 'Pashto, Pushto'),
        ('pt', 'Portuguese'), ('qu', 'Quechua'), ('rm', 'Romansh'), ('rn', 'Kirundi'),
        ('ro', 'Romanian, Moldavian, Moldovan'), ('ru', 'Russian'),
        ('sa', 'Sanskrit (Saṁskṛta)'), ('sc', 'Sardinian'), ('sd', 'Sindhi'),
        ('se', 'Northern Sami'), ('sm', 'Samoan'), ('sg', 'Sango'), ('sr', 'Serbian'),
        ('gd', 'Scottish Gaelic; Gaelic'), ('sn', 'Shona'), ('si', 'Sinhala, Sinhalese'),
        ('sk', 'Slovak'), ('sl', 'Slovene'), ('so', 'Somali'), ('st', 'Southern Sotho'),
        ('es', 'Spanish; Castilian'), ('su', 'Sundanese'), ('sw', 'Swahili'), ('ss', 'Swati'),
        ('sv', 'Swedish'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'),
        ('ti', 'Tigrinya'), ('bo', 'Tibetan Standard, Tibetan, Central'), ('tk', 'Turkmen'),
        ('tl', 'Tagalog'), ('tn', 'Tswana'), ('to', 'Tonga (Tonga Islands)'),
        ('tr', 'Turkish'), ('ts', 'Tsonga'), ('tt', 'Tatar'), ('tw', 'Twi'), ('ty', 'Tahitian'),
        ('ug', 'Uighur, Uyghur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'),
        ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'),
        ('cy', 'Welsh'), ('wo', 'Wolof'), ('fy', 'Western Frisian'), ('xh', 'Xhosa'),
        ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang, Chuang'), ('zu', 'Zulu'),
    ]
    native_language = models.CharField(
        max_length=20,
        choices=NATIVE_LANGUAGE_CHOICES,
        verbose_name='Native Language'
    )

    NATIONALITY_CHOICES = [
    ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'),
    ('AD', 'Andorra'), ('AO', 'Angola'), ('AR', 'Argentina'), ('AM', 'Armenia'),
    ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'),
    ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BY', 'Belarus'), ('BE', 'Belgium'),
    ('BZ', 'Belize'), ('BJ', 'Benin'), ('BT', 'Bhutan'), ('BO', 'Bolivia'),
    ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BR', 'Brazil'),
    ('BN', 'Brunei'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'),
    ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'),
    ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'),
    ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo (DRC)'),
    ('CR', 'Costa Rica'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'),
    ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GA', 'Gabon'),
    ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'),
    ('GR', 'Greece'), ('GD', 'Grenada'), ('GT', 'Guatemala'), ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HN', 'Honduras'),
    ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'),
    ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'),
    ('JM', 'Jamaica'), ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', 'North Korea'), ('KR', 'South Korea'),
    ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Laos'), ('LV', 'Latvia'),
    ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'),
    ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MG', 'Madagascar'),
    ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'),
    ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MR', 'Mauritania'), ('MU', 'Mauritius'),
    ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'), ('MC', 'Monaco'),
    ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MA', 'Morocco'), ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'),
    ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'),
    ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine'),
    ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'),
    ('PH', 'Philippines'), ('PL', 'Poland'), ('PT', 'Portugal'), ('QA', 'Qatar'),
    ('RO', 'Romania'), ('RU', 'Russia'), ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'),
    ('LC', 'Saint Lucia'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'),
    ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'), ('ZA', 'South Africa'), ('ES', 'Spain'), ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'), ('SR', 'Suriname'), ('SZ', 'Swaziland'), ('SE', 'Sweden'),
    ('CH', 'Switzerland'), ('SY', 'Syria'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'),
    ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'),
    ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'),
    ('VN', 'Vietnam'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'),
    ]

    nationality = models.CharField(
        max_length=50,
        choices=NATIONALITY_CHOICES,
        blank=True,
        verbose_name='Nationality'
    )


    # --- Advanced Profile (optional with privacy toggles) ---
    born_year = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Born Year'
    )
    show_born_year = models.BooleanField(
        default=False,
        verbose_name='Show Born Year'
    )

    nationality = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nationality'
    )
    show_nationality = models.BooleanField(
        default=False,
        verbose_name='Show Nationality'
    )

    favorite_categories = models.ManyToManyField(
        'Category',         # 또는 Category 모델이 같은 파일에 있으면 그냥 Category
        blank=True,
        verbose_name='관심 카테고리'
    )



    major = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Major'
    )
    show_major = models.BooleanField(
        default=False,
        verbose_name='Show Major'
    )

    instagram_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Instagram ID'
    )
    show_instagram = models.BooleanField(
        default=False,
        verbose_name='Show Instagram ID'
    )

    MBTI_CHOICES = [
        ('INTJ','INTJ'),('INTP','INTP'),('ENTJ','ENTJ'),('ENTP','ENTP'),
        ('INFJ','INFJ'),('INFP','INFP'),('ENFJ','ENFJ'),('ENFP','ENFP'),
        ('ISTJ','ISTJ'),('ISFJ','ISFJ'),('ESTJ','ESTJ'),('ESFJ','ESFJ'),
        ('ISTP','ISTP'),('ISFP','ISFP'),('ESTP','ESTP'),('ESFP','ESFP'),
    ]
    personality = models.CharField(
        max_length=4,
        choices=MBTI_CHOICES,
        blank=True,
        verbose_name='Personality'
    )
    show_personality = models.BooleanField(
        default=False,
        verbose_name='Show Personality'
    )


    bio = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Bio'
    )
    show_bio = models.BooleanField(
        default=False,
        verbose_name='Show Bio'
    )

    interests = models.ManyToManyField(
        Interest,
        blank=True,
        related_name='profiles',
        verbose_name='User-selected Interests'
    )

    # ─── 새로 담은(선택된) 토픽을 저장할 필드 ───
    selected_topics = models.ManyToManyField(
        Topic,
        blank=True,
        related_name='selected_by',
        verbose_name='User-selected Topics'
    )




    def __str__(self):
        return f'{self.user.username} - {self.nickname}'




class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendships_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendships_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.status})"
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)  # 조회수 필드

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
