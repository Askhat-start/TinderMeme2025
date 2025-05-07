# TinderMeme2025 — Мемный Tinder

**TinderMeme2025** — это оригинальное веб-приложение, сочетающее механику свайпов из Tinder с генерацией и подбором мемов. Пользователи могут лайкать/дизлайкать мемы, сохранять любимые, а также получать "мемные совпадения" по вкусу.

---

##  Основной функционал:
- Свайп система (лайк/дизлайк) для мемов
- Сохранение любимых мемов
- Автоматическое нахождение пользователей с похожими мем-вкусами
- Система аутентификации пользователей

---

## Технологии

| Компонент        | Описание                                       |
|------------------|------------------------------------------------|
| **Django**       | Python-фреймворк для построения backend + шаблонов |
| **SQLite**       | База данных (можно заменить на PostgreSQL)     |
| **HTML/CSS**     | Интерфейс и стили                               |
| **JavaScript (AJAX)** | Асинхронные запросы свайпов и сохранений  |

---

##  Процесс проектирования

### 1. Моделирование базы данных:

```python
class Meme(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateField(auto_now_add=True)
````

```python
class Swipe(models.Model):
    SWIPE_CHOICES = (('like', 'Like'), ('dislike', 'Dislike'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    action = models.CharField(choices=SWIPE_CHOICES, max_length=15)
    timestamp = models.DateField(auto_now_add=True)
```

```python
class SavedMemes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
```

```python
class Matches(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    matched_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matched_by")
    similarity_score = models.FloatField()
```

---

### 2. Навигация и структура URL

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Основные страницы:

* `/` — просмотр и свайп мемов
* `/matches/` — просмотр совпадений
* `/saved/` — просмотр сохранённых мемов
* `/accounts/` — регистрация и вход

---

### 3. Основные представления (views)

#### Свайп и фильтр по неоценённым мемам:

```python
def getUnswipedMemes(user):
    swiped_memes = Swipe.objects.filter(user=user).values('meme')
    return Meme.objects.exclude(id__in=Subquery(swiped_memes))[:10]
```

#### Сохрани мему и мем сохранит тебя:

```python
@csrf_exempt
@login_required
def save_meme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        meme_id = data.get('meme_id')
        meme = Meme.objects.get(id=meme_id)
        SavedMemes.objects.get_or_create(user=request.user, meme=meme)
        return JsonResponse({'status': 'saved'})
```

#### Алгоритм совпадений:

```python
def calculate_user_matches(user):
    liked_memes = Swipe.objects.filter(user=user, action='like').values_list('meme_id', flat=True)

    if liked_memes.count() < 10:
        return []

    matches = (
        Swipe.objects
        .filter(meme_id__in=liked_memes, action='like')
        .exclude(user=user)
        .values('user')
        .annotate(similarity_score=Count('meme'))
        .order_by('-similarity_score')
    )

    for match in matches:
        matched_user = User.objects.get(id=match['user'])
        Matches.objects.update_or_create(
            user=user,
            matched_with=matched_user,
            defaults={'similarity_score': match['similarity_score']}
        )
    return matches
```

---

## Установка и запуск проекта

### Предварительные требования:

* Python 3.x
* Django

### Установка:

```bash
git clone https://github.com/Askhat-start/TinderMeme2025.git
cd TinderMeme2025
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Перейдите в браузере по адресу: `http://127.0.0.1:8000/`

---

##  Компромиссы

* Использование SQLite вместо PostgreSQL для простоты запуска на начальных этапах.
* Нет API-интерфейса (REST), но логика построена так, что можно легко масштабировать с использованием DRF.
* Визуальное оформление минималистично: сделан упор на функциональность.

---

##  Возможные проблемы

* Низкая производительность базы данных. Фреймворк Django по умолчанию использует SQLLite базу данных что может сильно навредить оптимизации и скорости работы приложения
* Решение: Установка современной версии PostgreSQL с целью повышения технологического уровня.
* Низкий порог входа в совпадения (10 лайков), можно адаптировать под активность пользователей.

---

##  Почему именно этот стек?

* Django даёт полный набор инструментов из коробки: ORM, миграции, аутентификация, шаблоны.
* Простота интеграции с фронтом (HTML + JS).
* Pillow для обработки изображений без боли.
* Проект масштабируем: можно добавить WebSocket, Celery, Redis и DRF для расширения.

