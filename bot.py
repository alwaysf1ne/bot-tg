import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7554405811:AAGIOhdHMBZhhP1sd_dJHQ69f2B8RY7d-wo"
AUTHORIZED_USERS = {566236385: "Иван Иванов", 987654321: "Анна Петрова"}  # Telegram ID -> ФИО

user_data = {}  # Хранение данных о выборе услуги и чаевых

SERVICES_MEN = {
    "service_200_": "Стрижка «Наголо»",
    "service_250": "Стрижка под машинку «Бокс», «Полубокс»",
    "service_300": "С чёлкой, Стрижка под машинку «Бокс», «Полубокс»",
    "service_350": "Стрижка «Модельная», с переходом с нуля",
    "service_400": "Стрижка «Креативная»",
    "service_custom_50": "Нанесение рисунка",
    "service_custom_150": "Подравнивание усов/бороды",
    "service_100": "Мытье волос"
}

SERVICES_WOMEN_PAGE_1 = {
    "service_400_page1": "Стрижка «Модельная»",
    "service_450_page1": "Короткие, Стрижка «Каре», «Каскад», «Асимметрия»",
    "service_500_page1": "Средние, Стрижка «Каре», «Каскад», «Асимметрия»",
    "service_550_page1": "Длинные, Стрижка «Каре», «Каскад», «Асимметрия»",
    "service_600_page1": "Очень длинные, Стрижка «Каре», «Каскад», «Асимметрия»",
    "service_150_page1": "Подравнивание чёлки",
    "service_250_page1": "Подравнивание кончиков"
}

SERVICES_WOMEN_PAGE_2 = {
    "service_400_page2": "Подравнинивание кончиков (густые)",
    "service_150_brows_page2": "Брови оформление",
    "service_200_page2": "Брови окрашивание",
    "service_150_wash_page2": "Мытье волос шампунем с применением бальзама-ополаскивателя",
    "service_100_page2": "Короткие, Сушка волос",
    "service_150_page2": "Длинные, Сушка волос",
    "service_700_page2": "Короткие, Укладка волос"
}

SERVICES_WOMEN_PAGE_3 = {
    "service_900_1_page3": "Средние, Укладка волос",
    "service_1000_page3": "Длинные, Укладка волос",
    "service_900_2_page3": "Средние, Прическа",
    "service_1300_page3": "Длинные, Прическа",
    "service_1600_page3": "Очень длинные, Прическа",
    "service_700_page3": "Короткие, Локоны",
    "service_900_page3": "Средние, Локоны "
}

SERVICES_WOMEN_PAGE_4 = {
    "service_1100_page4": "Длинные, Локоны",
    "service_custom_300_page4": "Плетение кос",
    "service_900_page4": "Короткие, Окрашивание волос в один тон",
    "service_1300_page4": "Средние, Окрашивание волос в один тон",
    "service_1700_page4": "Длинные, Окрашивание волос в один тон",
    "service_2100_page4": "Очень длинные, Окрашивание волос в один тон",
    "service_2680_page4": "Средние, Сложное окрашивание волос"
}

SERVICES_WOMEN_PAGE_5 = {
    "service_4050_page5": "Длинные, Сложное окрашивание волос",
    "service_5420_page5": "Очень длинные, Сложное окрашивание волос",
    "service_2000_page5": "Сложное окрашивание прядей теменной (топовой) зоны",
    "service_1500_page5": "Короткие, Химическая завивка волос",
    "service_3000_page5": "Средние, Химическая завивка волос",
    "service_4200_page5": "Длинные, Химическая завивка волос"
}

# Главное меню
def main_menu():
    keyboard = [[InlineKeyboardButton("Добавить услугу", callback_data="add_service")],
                [InlineKeyboardButton("Личный кабинет", callback_data="profile")]]
    return InlineKeyboardMarkup(keyboard)


# Меню выбора зала
def service_menu():
    keyboard = [[InlineKeyboardButton("Мужской зал", callback_data="mens_hall")],
                [InlineKeyboardButton("Женский зал", callback_data="womens_hall")],
                [InlineKeyboardButton("Назад", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)


# Меню услуг Мужского зала
def mens_hall_menu():
    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)] for key, name in SERVICES_MEN.items()
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


# Меню услуг Женского зала (страница 1)
def womens_hall_menu_page_1():
    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)] for key, name in SERVICES_WOMEN_PAGE_1.items()
    ]
    keyboard.append([InlineKeyboardButton("След. страница", callback_data="womens_hall_menu_page_2")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


# Меню услуг Женского зала (страница 2)
def womens_hall_menu_page_2():
    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)] for key, name in SERVICES_WOMEN_PAGE_2.items()
    ]
    keyboard.append([InlineKeyboardButton("Пред. страница", callback_data="womens_hall_menu_page_1")])
    keyboard.append([InlineKeyboardButton("След. страница", callback_data="womens_hall_menu_page_3")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

# Меню услуг Женского зала (страница 3)
def womens_hall_menu_page_3():
    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)] for key, name in SERVICES_WOMEN_PAGE_3.items()
    ]
    keyboard.append([InlineKeyboardButton("Пред. страница", callback_data="womens_hall_menu_page_2")])
    keyboard.append([InlineKeyboardButton("След. страница", callback_data="womens_hall_menu_page_4")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

#Меню услуг Женского зала (страница 4)
def womens_hall_menu_page_4():
    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)] for key, name in SERVICES_WOMEN_PAGE_4.items()
    ]
    keyboard.append([InlineKeyboardButton("Пред. страница", callback_data="womens_hall_menu_page_3")])
    keyboard.append([InlineKeyboardButton("След. страница", callback_data="womens_hall_menu_page_5")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

# Меню услуг Женского зала (страница 5)
def womens_hall_menu_page_5():
    keyboard = [
        [InlineKeyboardButton(name, callback_data=key)] for key, name in SERVICES_WOMEN_PAGE_5.items()
    ]
    keyboard.append([InlineKeyboardButton("Пред. страница", callback_data="womens_hall_menu_page_4")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in AUTHORIZED_USERS:
        await update.message.reply_text("Выберите действие:", reply_markup=main_menu())
    else:
        await update.message.reply_text("Доступ запрещен")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "main_menu":
        await query.message.edit_text("Выберите действие:", reply_markup=main_menu())
    elif query.data == "add_service":
        await query.message.edit_text("Выберите зал:", reply_markup=service_menu())
    elif query.data == "mens_hall":
        await query.message.edit_text("Выберите услугу:", reply_markup=mens_hall_menu())
    elif query.data == "womens_hall":
        await query.message.edit_text("Выберите услугу:", reply_markup=womens_hall_menu_page_1())
    elif query.data.startswith("service_"):
        all_services = {**SERVICES_MEN, **SERVICES_WOMEN_PAGE_1, **SERVICES_WOMEN_PAGE_2,
                        **SERVICES_WOMEN_PAGE_3, **SERVICES_WOMEN_PAGE_4, **SERVICES_WOMEN_PAGE_5}
        service_name = all_services.get(query.data, "Неизвестная услуга")
        service_info = query.data.split("_")
        if service_info[1] == "custom":
            min_price = int(service_info[2])
            user_data[user_id] = {"service_name": service_name, "min_price": min_price}
            await query.message.edit_text(f"Введите стоимость услуги (от {min_price} рублей):")
        else:
            price = int(service_info[1])
            user_data[user_id] = {"service_name": service_name, "price": price}
            await query.message.edit_text("Введите сумму чаевых (или 0, если нет):")

    elif query.data == "profile":
        name = AUTHORIZED_USERS.get(user_id, "Неизвестный пользователь")
        await query.message.edit_text(f"Личный кабинет\nФИО: {name}\n[История за день]", reply_markup=main_menu())
    elif query.data == "confirm_service":
        await query.message.edit_text("Услуга добавлена!", reply_markup=main_menu())
        del user_data[user_id]
    elif query.data == "cancel_service":
        await query.message.edit_text("Добавление отменено.", reply_markup=main_menu())
        del user_data[user_id]
    elif query.data == "womens_hall_menu_page_1":
        await query.message.edit_text("Выберите услугу:", reply_markup=womens_hall_menu_page_1())
    elif query.data == "womens_hall_menu_page_2":
        await query.message.edit_text("Выберите услугу:", reply_markup=womens_hall_menu_page_2())
    elif query.data == "womens_hall_menu_page_3":
        await query.message.edit_text("Выберите услугу:", reply_markup=womens_hall_menu_page_3())
    elif query.data == "womens_hall_menu_page_4":
        await query.message.edit_text("Выберите услугу:", reply_markup=womens_hall_menu_page_4())
    elif query.data == "womens_hall_menu_page_5":
        await query.message.edit_text("Выберите услугу:", reply_markup=womens_hall_menu_page_5())


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data:
        if "min_price" in user_data[user_id]:
            try:
                price = int(update.message.text)
                if price < user_data[user_id]["min_price"]:
                    await update.message.reply_text(
                        f"Сумма должна быть не меньше {user_data[user_id]['min_price']} рублей. Введите заново:")
                    return
                user_data[user_id]["price"] = price
                del user_data[user_id]["min_price"]
                await update.message.reply_text("Введите сумму чаевых (или 0, если нет):")
            except ValueError:
                await update.message.reply_text("Пожалуйста, введите число.")
        else:
            try:
                tips = int(update.message.text)
                user_data[user_id]["tips"] = tips
                keyboard = [[InlineKeyboardButton("Подтвердить", callback_data="confirm_service")],
                            [InlineKeyboardButton("Отмена", callback_data="cancel_service")]]
                await update.message.reply_text(
                    f"Подтвердите услугу: {user_data[user_id]['service_name']}, чаевые {tips} рублей.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except ValueError:
                await update.message.reply_text("Пожалуйста, введите число.")


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
