dataset = {
    "choose_profile_type": {
        "message": "Choose your profile type:",

        "profile_types": {
            "passenger": "👤 Passenger",
            "driver": "🚗 Driver",
        },

        "error": "Please, choose one of the options.",
    },

    "register": {
        "enter_name": "Enter your name:",
        "enter_car_brand": "Enter your car brand:",
        "enter_seating_capacity": "Enter your car seating capacity:",
        "enter_is_child_seat": "Do you have a child seat?",

        "enter_about": "Tell us about yourself:",
        "is_it_correct": "Is it correct?",
        "driver_info": "Name: {name}\nCar brand: {car_brand}\nSeating capacity: {seating_capacity}\nChild seat: {"
                       "is_child_seat}\nAbout: {about}",

        "success_register": "You have successfully registered!",
    },

    "menus": {
        "main_menu": {
            "message": "Choose action:",
        },

        "passenger_my_profile_menu": {
            "message": "Your profile info:\n\nName: {0}",
        },

        "driver_my_profile_menu": {
            "message": "Name: {name}\nCar brand: {car_brand}\nSeating capacity: {seating_capacity}\nChild seat: {"
                       "has_child_seat}\nAbout: {about}\n\nYour location: {geo_position}\nSearch radius: {"
                       "active_radius} km\n\n"
                       "Active: {is_active}",
        },
    },

    "edit_name": {
        "message": "Enter your new name:",
        "success": "Name changed successfully.",
    },

    "edit_data": {
        "success": "Data changed successfully.",
    },

    "set_my_geo_position": {
        "message": "Send your location:",
        "success": "Location set successfully. Your location: {geo_position}",
        "error": "Message has no location. Location not set.",

        "radius": "Enter your search radius (km):",
        "success_radius": "Search radius set successfully. Your search radius: {active_radius} km",
        "error_radius": "Please, enter a number.",
    },

    "delete_profile": {
        "message": "Are you sure you want to delete your profile?",
        "success": "Profile deleted successfully.",
        "cancel": "Profile deletion canceled.",
    },

    "change_language": {
        "message": "Choose your language:",
        "success": "Language changed successfully.",
        "error": "Please, choose one of the options.",
    },

    "nearby_drivers_count": {
        "message": "Near you: {count} drivers.",
        "send_location": "Send your location.",
    },

    "call_driver": {
        "send_location": "Send your departure point:",
        "send_destination": "Send your destination point:",

        "send_passengers_count": "Enter the number of passengers:",
        "do_you_have_baggage": "Do you have baggage?",
        "do_you_need_child_seat": "Do you need a child seat?",

        "drivers_list": "Drivers list:",
        "driver_info": "Name: {name}\nCar brand: {car_brand}\nChild seat: {has_child_seat}"
                       "\nAbout: {about}\nDistance: {distance} km",

        "no_drivers": "Unfortunately, there are no drivers near you. Try again later.",

        "driver_chosen": "You have chosen driver {name}.",

        "message_dont_have_location": "Message has no location. Point not set.",
    },

    "yes": "Yes",
    "no": "No",
    "unknown": "Unknown",
    "undefined": "Undefined",

    "duty": {
        "now_you_online": "🟢 You are on duty.",
        "now_you_offline": "🔴 You left duty.",
    },

    "errors": {
        "unknown": "An error occurred. Please try again later.",
        "not_registered": "You are not registered in our system. Please, register first.",
        "choose_from_list": "Please, choose one of the options.",
        "enter_number": "Please, enter a number.",
        "enter_location": "Please, send your location.",
    },

    "keyboards": {
        "register": {
            "register": "Register",
        },
        "main_menu": {
            "passenger": {
                "my_profile": "👤 My profile",
                "call_taxi": "🚕 Call taxi",
                "book_taxi": "📅 Book taxi",
                "get_nearby_drivers_count": "👨‍✈️ Get nearby drivers count",
            },
            "driver": {
                "my_profile": "🚗 My profile",
                "set_my_geo_position": "📍 Set my geo position",
                "go_online": "🟢 Go online",
                "go_offline": "🔴 Go offline",
                "get_nearby_drivers_count": "👨‍✈️ Get nearby drivers count",
            },
        },
        "passenger_my_profile_menu": {
            "edit_name": "✏️ Edit name",
            "delete_profile": "❌ Delete profile",
            "change_language": "🌐 Change language",
            "back": "🔙 Back",
        },

        "driver_my_profile_menu": {
            "edit_data": "✏️ Edit data",
            "delete_profile": "❌ Delete profile",
            "change_language": "🌐 Change language",
            "back": "🔙 Back",
        },
        "call_driver": {
            "choose_driver": "🟢 Choose driver",
        },
    }
}
