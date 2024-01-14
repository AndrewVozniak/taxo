dataset = {
    "choose_profile_type": {
        "message": "Выберите тип профиля:",

        "profile_types": {
            "passenger": "👤 Пассажир",
            "driver": "🚗 Водитель",
        },

        "error": "Пожалуйста, выберите один из вариантов.",
    },

    "register": {
        "enter_name": "Введите ваше имя:",
        "enter_car_brand": "Введите марку вашего автомобиля:",
        "enter_seating_capacity": "Введите количество мест в вашем автомобиле:",
        "enter_is_child_seat": "У вас есть детское кресло?",

        "enter_about": "Расскажите о себе:",
        "is_it_correct": "Все верно?",
        "driver_info": "Имя: {name}\nМарка автомобиля: {car_brand}\nКоличество мест: {seating_capacity}\nДетское "
                       "кресло: "
                       "{is_child_seat}\nО себе: {about}",

        "success_register": "Вы успешно зарегистрированы!",
    },

    "menus": {
        "main_menu": {
            "message": "Выберите действие:",
        },

        "passenger_my_profile_menu": {
            "message": "Информация о вашем профиле:\n\nИмя: {0}",
        },

        "driver_my_profile_menu": {
            "message": "Имя: {name}\nМарка автомобиля: {car_brand}\nКоличество мест: {seating_capacity}\nДетское "
                       "кресло: "
                       "{has_child_seat}\nО себе: {about}\n\nВаша геолокация: {geo_position}\nРадиус "
                       "поиска: {active_radius} км\n\nАктивен: {is_active}",
        },
    },

    "edit_name": {
        "message": "Введите ваше новое имя:",
        "success": "Имя успешно изменено.",
    },

    "edit_data": {
        "success": "Данные успешно изменены.",
    },

    "set_my_geo_position": {
        "message": "Отправьте вашу геолокацию:",
        "success": "Геолокация успешно установлена. Ваша геолокация: {geo_position}",
        "error": "Сообщение не содержит геолокацию. Геолокация не установлена.",

        "radius": "Введите радиус поиска (км):",
        "success_radius": "Радиус поиска успешно установлен. Ваш радиус поиска: {active_radius} км",
        "error_radius": "Пожалуйста, введите число.",
    },

    "delete_profile": {
        "message": "Вы уверены, что хотите удалить свой профиль?",
        "success": "Профиль успешно удален.",
        "cancel": "Удаление профиля отменено.",
    },

    "change_language": {
        "message": "Выберите язык:",
        "success": "Язык успешно изменен.",
        "error": "Пожалуйста, выберите один из вариантов.",
    },

    "yes": "Да",
    "no": "Нет",
    "undefined": "Не указано",
    "unknown": "Неизвестно",

    "duty": {
        "now_you_online": "🟢 Вы вступили на дежурство.",
        "now_you_offline": "🔴 Вы вышли из дежурства.",
    },

    "errors": {
        "unknown": "Произошла ошибка. Пожалуйста, попробуйте позже.",
        "not_registered": "Вы не зарегистрированы в нашей системе. Пожалуйста, зарегистрируйтесь.",
        "choose_from_list": "Пожалуйста, выберите один из вариантов.",
        "enter_number": "Пожалуйста, введите число.",
    },

    "keyboards": {
        "register": {
            "register": "Зарегистрироваться",
        },
        "main_menu": {
            "passenger": {
                "my_profile": "👤 Мой профиль",
                "call_taxi": "🚕 Вызвать такси",
                "book_taxi": "📅 Забронировать такси",
                "get_nearby_drivers_count": "👨‍✈️ Узнать количество дежурных таксистов поблизу",
            },
            "driver": {
                "my_profile": "🚗 Мой профиль",
                "set_my_geo_position": "📍 Указать мою геолокацию",
                "go_online": "🟢 Вступить на дежурство",
                "go_offline": "🔴 Выйти из дежурства",
                "get_nearby_drivers_count": "👨‍✈️ Узнать количество дежурных таксистов поблизу",
            },
        },
        "passenger_my_profile_menu": {
            "edit_name": "✏️ Редактировать имя",
            "delete_profile": "❌ Удалить профиль",
            "change_language": "🌐 Изменить язык",
            "back": "🔙 Назад",
        },
        "driver_my_profile_menu": {
            "edit_data": "✏️ Обновить данные",
            "delete_profile": "❌ Удалить профиль",
            "change_language": "🌐 Изменить язык",
            "back": "🔙 Назад",
        },
    }
}
