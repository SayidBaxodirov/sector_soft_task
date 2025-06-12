# 📦 Sector Soft Task

Sector soft uchun Python Django va python-telegram-bot vazifasi.

---

## 🌐 Online do'kon uchun telegram bot va admin panelga API 

Proyekt **Django REST Framework** va Python Telegram Bot v21 yordamida yasalgan va foydalanuvchilar bot orqali quyidagilarni qilishlari mumkin:

- Kategoriyalarni ko'rish;
- Mahsulotlar va ularni tafsilotlarini ko'rish;
- Mahsulotlarning har xil ranglarini ko'rish va ularni savatchaga qo'shish yoki olib tashlash;

---

## 🚀 Proyektni ishga tushirish

1. **Repositoryni klon qiling**

```bash
git clone https://github.com/SayidBaxodirov/sector_soft_task.git
cd sector_soft_task
```
2. **`.env` faylini yarating va unga kerakli ma'lumotlarni qo'shing**\
Quyidagilarni yozishingiz kerak:\
DEBUG=\
SECRET_KEY=\
TELEGRAM_BOT_TOKEN=

3. **Docker orqali proyektni boshlang**
```bash
docker-compose up --build
```
4. **Superuser yarating**
```
docker-compose exec web python manage.py createsuperuser
```
Nomer, ismingiz va parolni kiritishingiz kerak bo'ladi

---

## 🧪 API ni tekshirish
Proyektni boshlaganingizdan keyin API quyidagi manzil orqali ko'rinadi:
http://127.0.0.1:8000/api/
### Autentifikatsiyadan o'tish uchun:
1. **Quyidagi manzilni oching**\
http://127.0.0.1:8000/api-auth/login

2. **Superuser ma'lumotlarini kiriting**\
Nomer va parolni kiritishingiz kerak bo'ladi

**Endi saytda POST, PUT, PATCH, DELETE ishlatishingiz mumkin.**

__Saytdan chiqish uchun:__
http://127.0.0.1:8000/api-auth/logout
## 📫 Bog'lanish uchun
Muallif: __Sayidabdullaxon Baxodirov__



