from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
from datetime import datetime, timedelta

class AutoBookingSimulator:
    def __init__(self):
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        # Initialize driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Test data
        self.user_data = {
            'name': 'Erik Andersson',
            'company': 'TechSoft AB',
            'email': 'erik@techsoft.se',
            'phone': '+46701234567',
            'message': 'Vi är intresserade av att implementera en AI-driven kundtjänstlösning.'
        }

    def start_simulation(self):
        try:
            print("\n=== Starting Automated Booking Simulation ===\n")
            
            # Open the chat interface
            self.driver.get("http://127.0.0.1:3000")
            time.sleep(2)  # Wait for chat to initialize
            
            print("Watching chat conversation...")
            # Wait for booking modal to appear
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "booking-modal")))
            print("Booking modal detected!")
            
            # Simulate booking process
            self.simulate_booking()
            
            # Wait for paper plane animation
            time.sleep(5)
            print("\n=== Simulation Complete ===")
            
        except Exception as e:
            print(f"Error during simulation: {e}")
        finally:
            time.sleep(3)  # Keep browser open briefly to see results
            self.driver.quit()

    def simulate_booking(self):
        print("\nStarting booking process...")
        
        # Step 1: Select Date and Time
        print("Step 1: Selecting date and time")
        self.select_date_and_time()
        time.sleep(1)
        
        # Click Next
        next_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "next-button")))
        next_button.click()
        time.sleep(1)
        
        # Step 2: Fill Form
        print("Step 2: Filling contact information")
        self.fill_contact_form()
        time.sleep(1)
        
        # Click Next to go to confirmation
        next_buttons = self.driver.find_elements(By.CLASS_NAME, "next-button")
        next_buttons[-1].click()
        time.sleep(1)
        
        # Step 3: Confirm Booking
        print("Step 3: Confirming booking")
        confirm_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "confirm-button")))
        time.sleep(1)  # Brief pause before confirming
        confirm_button.click()
        
        print("✓ Booking confirmed!")

    def select_date_and_time(self):
        # Wait for calendar to be visible
        calendar = self.wait.until(EC.presence_of_element_located((By.ID, "calendar")))
        
        # Find and select a date (the pre-selected Tuesday)
        selected_date = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "day.selected")))
        print(f"Selected date: {selected_date.text}")
        
        # Select time slot (10:00 is pre-selected)
        time_slots = self.driver.find_elements(By.CLASS_NAME, "time-slot")
        selected_time = next(slot for slot in time_slots if "selected" in slot.get_attribute("class"))
        print(f"Selected time: {selected_time.text}")

    def fill_contact_form(self):
        # Fill each form field with typing animation
        form_fields = {
            'Ditt namn': self.user_data['name'],
            'Företagsnamn': self.user_data['company'],
            'din@epost.se': self.user_data['email'],
            '+46': self.user_data['phone']
        }
        
        for placeholder, value in form_fields.items():
            field = self.driver.find_element(By.CSS_SELECTOR, f'input[placeholder="{placeholder}"]')
            self.simulate_typing(field, value)
        
        # Fill message field
        message_field = self.driver.find_element(By.TAG_NAME, 'textarea')
        self.simulate_typing(message_field, self.user_data['message'])

    def simulate_typing(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))  # Random delay between keystrokes

if __name__ == "__main__":
    simulator = AutoBookingSimulator()
    simulator.start_simulation() 