import time
import random
from datetime import datetime, timedelta
import json

class BookingSimulator:
    def __init__(self):
        self.user_data = {
            'names': ['Erik Andersson', 'Maria Nilsson', 'Johan Lindberg', 'Anna Karlsson', 'Lars Eriksson'],
            'companies': ['TechSoft AB', 'Digital Solutions', 'Innovation Tech', 'Svenska IT AB', 'Future Systems'],
            'emails': ['erik@techsoft.se', 'maria@digitalsolutions.se', 'johan@innovation.se', 'anna@svenskait.se', 'lars@future.se'],
            'phones': ['+46701234567', '+46723456789', '+46734567890', '+46745678901', '+46756789012']
        }

    def get_next_available_tuesday(self):
        current_date = datetime.now()
        days_ahead = 1 - current_date.weekday()  # Tuesday is 1
        if days_ahead <= 0:
            days_ahead += 7
        next_tuesday = current_date + timedelta(days=days_ahead)
        return next_tuesday

    def simulate_booking(self):
        print("\n=== Starting Booking Simulation ===\n")
        
        # Step 1: Select Date and Time
        print("Step 1: Selecting Date and Time")
        next_tuesday = self.get_next_available_tuesday()
        selected_date = next_tuesday
        available_times = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"]
        selected_time = random.choice(available_times)
        
        print(f"Selected Date: {selected_date.strftime('%A, %d %B %Y')}")
        print(f"Selected Time: {selected_time}")
        time.sleep(1.5)
        
        # Step 2: Enter Personal Information
        print("\nStep 2: Entering Personal Information")
        user_index = random.randint(0, len(self.user_data['names']) - 1)
        booking_info = {
            'name': self.user_data['names'][user_index],
            'company': self.user_data['companies'][user_index],
            'email': self.user_data['emails'][user_index],
            'phone': self.user_data['phones'][user_index],
            'message': "Vi är intresserade av att implementera en AI-driven kundtjänstlösning."
        }
        
        print("Entering user details:")
        for key, value in booking_info.items():
            print(f"{key.capitalize()}: {value}")
            time.sleep(0.5)
        
        # Step 3: Confirmation
        print("\nStep 3: Confirming Booking")
        print("\nBooking Summary:")
        print("-" * 40)
        print(f"Date: {selected_date.strftime('%A, %d %B %Y')}")
        print(f"Time: {selected_time}")
        print(f"Name: {booking_info['name']}")
        print(f"Company: {booking_info['company']}")
        print(f"Email: {booking_info['email']}")
        print(f"Phone: {booking_info['phone']}")
        print("-" * 40)
        
        time.sleep(1)
        print("\nConfirming booking...")
        time.sleep(0.5)
        print("✓ Booking confirmed!")
        print("✓ Confirmation email sent")
        
        # Save booking to file
        booking_data = {
            'date': selected_date.strftime('%Y-%m-%d'),
            'time': selected_time,
            **booking_info
        }
        
        try:
            with open('bookings.json', 'r') as f:
                bookings = json.load(f)
        except FileNotFoundError:
            bookings = []
        
        bookings.append(booking_data)
        
        with open('bookings.json', 'w', encoding='utf-8') as f:
            json.dump(bookings, f, ensure_ascii=False, indent=2)
        
        print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    simulator = BookingSimulator()
    simulator.simulate_booking() 