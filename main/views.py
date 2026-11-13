import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password

from main.models import Card, User

# Спільний список карток
cards = [
    {
        "id": 1,
        "name": "Розділ 1",
        "image": "django.png",
        "description": "Розділ 1 присвячений вивченню веб-фреймворку Django для мови Python."
    },
    {
        "id": 2,
        "name": "Розділ 2",
        "image": "fastapi.png",
        "description": "Розділ 2 присвячений сучасному та швидкому фреймворку FastAPI."
    },
    {
        "id": 3,
        "name": "Розділ 3",
        "image": "flask.png",
        "description": "Розділ 3 присвячений легкому мікрофреймворку Flask."
    },
]


def home(request):
    return render(request, 'main/index.html', {"cards": cards})


def about(request):
    text = 'Це сторінка про нас'
    frameworks = ["django", "flask", "fastapi"]
    return render(request, 'main/about.html', {'frameworks': frameworks, 'text': text, 'data': [1, 2, 5, 7, 10, 100]}, )


def get_card(request, id):
    # Пошук за id або за індексом
    found_card = None
    for card in cards:
        if card.get("id") == id:
            found_card = card
            break

    if not found_card and 0 <= id < len(cards):
        found_card = cards[id]

    if found_card:
        return render(request, 'main/card.html', {'card': found_card})
    else:
        return render(request, 'main/not_found.html', {'query': f'ID: {id}'})


def search(request):
    # Отримуємо назву з GET або POST параметрів (підтримуємо name, q, title)
    query = (
            request.GET.get('name')
            or request.GET.get('q')
            or request.GET.get('title')
            or request.POST.get('name')
            or request.POST.get('q')
            or request.POST.get('title')
            or ''
    ).strip()

    if not query:
        return render(request, 'main/not_found.html', {'query': query})

    found_card = None
    query_lower = query.lower()

    # 1. Точний збіг за назвою (без урахування регістру)
    for card in cards:
        if card['name'].strip().lower() == query_lower:
            found_card = card
            break

    # 2. Частковий збіг за назвою
    if not found_card:
        for card in cards:
            if query_lower in card['name'].strip().lower():
                found_card = card
                break

    # 3. Збіг за назвою технології або зображення (наприклад, django, flask, fastapi)
    if not found_card:
        for card in cards:
            img_name = card.get('image', '').rsplit('.', 1)[0].lower()
            if query_lower == img_name or query_lower in img_name:
                found_card = card
                break

    if found_card:
        return render(request, 'main/card.html', {'card': found_card, 'query': query})
    else:
        return render(request, 'main/not_found.html', {'query': query})


def search_by_name(request, name):
    # Додатковий зручний маршрут пошуку через URL: /search/<name>/
    request.GET = request.GET.copy()
    request.GET['name'] = name
    return search(request)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        avatar = request.FILES.get('avatar')

        if not username or not email or not password:
            return JsonResponse({'status': 'error', 'message': 'Будь ласка, заповніть усі обов\'язкові поля!'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Користувач з таким ім\'ям вже існує!'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Користувач з такою поштою вже існує!'}, status=400)

        user = User(
            username=username,
            email=email,
            password=make_password(password),
            avatar=avatar
        )
        user.save()

        return JsonResponse({'status': 'success', 'message': f'Користувача {user.username} успішно зареєстровано!'})

    return render(request, 'main/register.html')

