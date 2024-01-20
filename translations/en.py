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

    "you_have_been_blocked": "Too many attempts. You have been blocked for {block_duration} minutes.",

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

        "you_choose_driver": "The driver has been chosen.\n\n"
                             "You will be notified when the driver accepts your request.",

        "you_were_chosen": "You were chosen by {name}."
                           "\n\nDeparture point: {location}"
                           "\nDestination point: {destination}"
                           "\n\nPassengers count: {passengers_count}"
                           "\nBaggage: {baggage}"
                           "\nChild seat: {child_seat}"
                           "\n\nTo accept the request, click the button below.",

        "trip_accepted_passenger": "Your order has been accepted by the driver {name}.",
        "trip_accepted_driver": "You accepted the order of the passenger {name}. \n"
                                "Telegram for communication: @{telegram_username}. \n\n"
                                "When you arrive at the departure point, click the button below.",

        "time_over_cancel": "The time for accepting the order has expired. The order has been canceled.",
        "time_over_cancel_driver": "The time for accepting the order from the passenger {name} has expired. \n\n"
                                   "The order has been canceled.",

        "you_can_cancel": "You can cancel the order by clicking the button below.",
        "you_cancel": "You canceled the order.",
        "trip_canceled": "The order was canceled.",
        "cant_cancel": "You cannot cancel the order because the driver has already arrived at the departure point.",

        "driver_arrived_driver": "You arrived at the departure point. \n\n "
                                 "When the passenger gets into the car, click the button below.",
        "driver_arrived_passenger": "The driver has arrived at the departure point. Please, go to the car.",

        "trip_started_driver": "You started the trip. \n\n When you arrive at the destination, click the button below.",
        "trip_started_passenger": "The trip has started.",
        "trip_ended": "The trip is over. Thank you for using our service!",

        "booking": {
            "send_date": "Send your trip date:",
            "send_time": "Send your trip time:",
            "booking_sent": "Your booking has been sent to drivers. \n\n",
            "booking_details": "You have received a booking from the passenger {name}.\n\n"
                               "Departure point: {location}\n"
                               "Destination point: {destination}\n\n"
                               "Passengers count: {passengers_count}\n"
                               "Baggage: {baggage}\n"
                               "Child seat: {child_seat}\n\n"
                               "Date: {date}\n"
                               "Time: {time}\n\n"
                               "To accept the booking, click the button below.",

            "booking_accepted_driver": "Booking from {name} accepted.\n\n"
                                       "Client's telegram: @{telegram_username}.\n"
                                       "Please, contact the client.",
            "booking_accepted_passenger": "Your booking has been accepted by the driver.\n\n"
                                          "Driver will contact you soon.",
        }
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

    "action_canceled": "Action canceled.",

    "keyboards": {
        "cancel": "❌ Cancel",

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
            "submit": "✅ Submit",
            "cancel_trip": "❌ Cancel trip",
            "im_arrived": "🚗 I'm arrived",
            "start_trip": "🚕 Start trip",
            "end_trip": "🏁 End trip",

            "booking": {
                "submit": "✅ Submit",
            }
        },
    }
}
