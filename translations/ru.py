
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

    "you_have_been_blocked": "Вы заблокированы на {block_duration} минут из-за частых попыток вызова.",

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

    "nearby_drivers_count": {
        "message": "Рядом с вами: {count} водителей.",
        "send_location": "Отправьте вашу геолокацию.",
    },

    "call_driver": {
        "send_location": "Отправьте точку отправления:",
        "send_destination": "Отправьте точку назначения:",

        "send_passengers_count": "Введите количество пассажиров:",
        "do_you_have_baggage": "У вас есть багаж?",
        "do_you_need_child_seat": "Вам нужно детское кресло?",

        "drivers_list": "Список водителей:",
        "driver_info": "Имя: {name}\nМарка автомобиля: {car_brand}\nДетское кресло: {has_child_seat}"
                       "\n\nО водителе: {about} "
                       "\n\nРасстояние до вас: {distance} км",

        "no_drivers": "К сожалению, рядом с вами нет водителей. Попробуйте позже.",

        "driver_chosen": "Вы выбрали водителя {name}.",

        "message_dont_have_location": "Сообщение не содержит геолокацию. Точка не установлена.",

        "you_choose_driver": "Водитель был выбран.\n\n"
                             "Вы будете оповещены, когда водитель примет ваш заказ.\n\n",

        "you_were_chosen": "Вас выбрал заказчик {name}.\n\n"
                           "Точка отправления: {location}\n"
                           "Точка назначения: {destination}\n\n"
                           "Количество пассажиров: {passengers_count}\n"
                           "Багаж: {baggage}\n"
                           "Детское кресло: {child_seat}\n\n"
                           "Чтобы принять заказ, нажмите кнопку ниже.",

        "trip_accepted_passenger": "Ваш вызов принят водителем {name}.\n\n",
        "trip_accepted_driver": "Вы приняли вызов пассажира {name}.\n"
                                "Телеграм для связи с заказчиком: @{telegram_username}.\n\n"
                                "Когда вы подъедете к пассажиру, нажмите кнопку ниже.",

        "time_over_cancel": "Время на принятие заказа истекло. Вызов отменен.",
        "time_over_cancel_driver": "Время на принятие заказа от пассажира {name} истекло. Вызов отменен.",

        "you_can_cancel": "Вы можете отменить вызов, нажав кнопку ниже.",
        "you_cancel": "Вы отменили вызов.",
        "trip_canceled": "Вызов отменен.",
        "cant_cancel": "Вы не можете отменить вызов, так как водитель уже приехал на место.",

        "driver_arrived_driver": "Вы прибыли. \n\n Когда пассажир сядет в машину, нажмите кнопку ниже.",
        "driver_arrived_passenger": "Водитель прибыл. \n\n Пожалуйста, подойдите к машине.",

        "trip_started_driver": "Вы начали поездку. \n\n Когда вы прибудете к месту назначения, нажмите кнопку ниже.",
        "trip_started_passenger": "Водитель начал поездку.",
        "trip_ended": "Вы завершили поездку. \n\n Спасибо за использование нашего сервиса!",

        "booking": {
            "send_date": "Отправьте дату поездки:",
            "send_time": "Отправьте время поездки:",
            "booking_sent": "Ваша бронь отправлена водителям. \n\n",
            "booking_details": "Вам поступила бронь от пассажира {name}.\n\n"
                               "Точка отправления: {location}\n"
                               "Точка назначения: {destination}\n\n"
                               "Количество пассажиров: {passengers_count}\n"
                               "Багаж: {baggage}\n"
                               "Детское кресло: {child_seat}\n\n"
                               "Дата отбытия: {date}\n"
                               "Время отбытия: {time}\n\n"
                               "Чтобы принять бронь, нажмите кнопку ниже.",

            "booking_accepted_driver": "Вы приняли бронь от пассажира {name}.\n\n"
                                       "Телеграм для связи с заказчиком: @{telegram_username}.\n"
                                       "Когда вы подъедете к пассажиру, нажмите кнопку ниже.",
            "booking_accepted_passenger": "Ваша бронь принята водителем.\n\n"
                                          "Ожидайте обратной связи от водителя.",
        },
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
        "enter_location": "Пожалуйста, отправьте геолокацию.",
    },

    "action_canceled": "Действие отменено.",

    "keyboards": {
        "cancel": "❌ Отменить",

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
        "call_driver": {
            "choose_driver": "🟢 Выбрать водителя",
            "submit": "✅ Принять заказ",
            "cancel_trip": "❌ Отменить поездку",
            "im_arrived": "🚗 Я прибыл",
            "start_trip": "🚕 Начать поездку",
            "end_trip": "🏁 Завершить поездку",

            "booking": {
                "submit": "✅ Принять бронь",
            }
        },
    }
}
