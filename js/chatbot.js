class AxieChatbot {
    constructor() {
        this.isOpen = false;
        this.currentStep = 1;
        this.selectedDate = null;
        this.selectedTime = null;
        this.bookingData = {};
        this.conversationStarted = false;
        
        this.initializeElements();
        this.bindEvents();
        this.startConversation();
    }

    initializeElements() {
        // Main elements
        this.chatButton = document.getElementById('chatButton');
        this.chatInterface = document.getElementById('chatInterface');
        this.minimizeBtn = document.getElementById('minimizeBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        // Booking modal elements
        this.bookingModal = document.getElementById('bookingModal');
        this.calendarGrid = document.getElementById('calendarGrid');
        this.timeSlots = document.getElementById('timeSlots');
        this.contactForm = document.getElementById('contactForm');
        
        // Animation elements
        this.paperPlaneAnimation = document.getElementById('paperPlaneAnimation');
        this.successOverlay = document.getElementById('successOverlay');
    }

    bindEvents() {
        // Chat interface events
        this.chatButton.addEventListener('click', () => this.openChat());
        this.minimizeBtn.addEventListener('click', () => this.closeChat());
        
        // Booking modal events
        this.bindBookingEvents();
        
        // Form validation
        this.bindFormValidation();
    }

    bindBookingEvents() {
        // Step navigation
        document.getElementById('nextToTime').addEventListener('click', () => this.nextStep());
        document.getElementById('backToDate').addEventListener('click', () => this.prevStep());
        document.getElementById('nextToForm').addEventListener('click', () => this.nextStep());
        document.getElementById('backToTime').addEventListener('click', () => this.prevStep());
        document.getElementById('nextToConfirm').addEventListener('click', () => this.nextStep());
        document.getElementById('backToForm').addEventListener('click', () => this.prevStep());
        document.getElementById('confirmBooking').addEventListener('click', () => this.confirmBooking());
        
        // Calendar navigation
        document.getElementById('prevMonth').addEventListener('click', () => this.changeMonth(-1));
        document.getElementById('nextMonth').addEventListener('click', () => this.changeMonth(1));
    }

    bindFormValidation() {
        const requiredFields = ['fullName', 'email'];
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            field.addEventListener('input', () => this.validateForm());
        });
    }

    async startConversation() {
        if (this.conversationStarted) return;
        this.conversationStarted = true;

        // Wait a moment then start the conversation
        await this.delay(2000);
        
        const conversation = [
            { text: "Hej! Välkommen till Axie Studio! 👋", isBot: true, delay: 1000 },
            { text: "Vi hjälper företag att implementera AI-lösningar för bättre kundservice.", isBot: true, delay: 2000 },
            { text: "Hej! Det låter intressant. Kan ni hjälpa oss?", isBot: false, delay: 1500 },
            { text: "Absolut! Vi skulle gärna visa er vad vi kan göra.", isBot: true, delay: 1800 },
            { text: "Har ni tid för en kort demo någon gång?", isBot: true, delay: 1200 },
            { text: "Ja, det skulle vara perfekt!", isBot: false, delay: 1000 },
            { text: "Fantastiskt! Låt mig hjälpa er att boka en tid. 📅", isBot: true, delay: 1500 },
        ];

        for (const message of conversation) {
            if (message.isBot) {
                await this.showTyping();
                await this.delay(1500);
                await this.hideTyping();
                await this.addBotMessage(message.text);
            } else {
                await this.simulateUserTyping(message.text);
                await this.addUserMessage(message.text);
            }
            await this.delay(message.delay);
        }

        // Open booking modal after conversation
        await this.delay(1000);
        await this.openBookingModal();
    }

    async openChat() {
        this.isOpen = true;
        this.chatButton.classList.add('hidden');
        this.chatInterface.classList.add('active');
        
        // Remove notification badge
        const badge = this.chatButton.querySelector('.notification-badge');
        if (badge) {
            badge.style.display = 'none';
        }
    }

    async closeChat() {
        this.isOpen = false;
        this.chatInterface.classList.remove('active');
        
        await this.delay(500);
        this.chatButton.classList.remove('hidden');
    }

    async showTyping() {
        this.typingIndicator.classList.add('active');
        this.scrollToBottom();
    }

    async hideTyping() {
        this.typingIndicator.classList.remove('active');
    }

    async addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';
        
        const textSpan = document.createElement('span');
        messageDiv.appendChild(textSpan);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString('sv-SE', {
            hour: '2-digit',
            minute: '2-digit'
        });
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.insertBefore(messageDiv, this.typingIndicator);
        
        // Type text character by character
        await this.typeText(textSpan, text);
        this.scrollToBottom();
    }

    async addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        
        const textSpan = document.createElement('span');
        textSpan.textContent = text;
        messageDiv.appendChild(textSpan);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString('sv-SE', {
            hour: '2-digit',
            minute: '2-digit'
        });
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.insertBefore(messageDiv, this.typingIndicator);
        this.scrollToBottom();
    }

    async typeText(element, text) {
        const words = text.split(' ');
        for (let i = 0; i < words.length; i++) {
            if (i > 0) element.textContent += ' ';
            const word = words[i];
            for (const char of word) {
                element.textContent += char;
                await this.delay(30);
            }
            await this.delay(100);
        }
    }

    async simulateUserTyping(text) {
        this.messageInput.value = '';
        this.messageInput.disabled = false;
        
        for (const char of text) {
            this.messageInput.value += char;
            await this.delay(80);
        }
        
        await this.delay(300);
        this.messageInput.value = '';
        this.messageInput.disabled = true;
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async openBookingModal() {
        this.bookingModal.classList.add('active');
        this.generateCalendar();
        this.generateTimeSlots();
    }

    closeBookingModal() {
        this.bookingModal.classList.remove('active');
    }

    generateCalendar() {
        const today = new Date();
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();
        
        // Update month header
        const monthNames = [
            'Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni',
            'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December'
        ];
        document.getElementById('currentMonth').textContent = `${monthNames[currentMonth]} ${currentYear}`;
        
        // Clear calendar
        this.calendarGrid.innerHTML = '';
        
        // Add day headers
        const dayHeaders = ['Mån', 'Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön'];
        dayHeaders.forEach(day => {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day header';
            dayElement.textContent = day;
            this.calendarGrid.appendChild(dayElement);
        });
        
        // Get first day of month and number of days
        const firstDay = new Date(currentYear, currentMonth, 1);
        const lastDay = new Date(currentYear, currentMonth + 1, 0);
        const startDate = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
        
        // Add empty cells for days before month starts
        for (let i = 0; i < startDate; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day';
            this.calendarGrid.appendChild(emptyDay);
        }
        
        // Add days of the month
        for (let day = 1; day <= lastDay.getDate(); day++) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;
            
            const dayDate = new Date(currentYear, currentMonth, day);
            const isToday = dayDate.toDateString() === today.toDateString();
            const isPast = dayDate < today;
            const isWeekend = dayDate.getDay() === 0 || dayDate.getDay() === 6;
            
            if (isToday) {
                dayElement.classList.add('today');
            }
            
            if (isPast || isWeekend) {
                dayElement.classList.add('disabled');
            } else {
                dayElement.classList.add('available');
                dayElement.addEventListener('click', () => this.selectDate(day, dayDate));
            }
            
            this.calendarGrid.appendChild(dayElement);
        }
        
        // Auto-select next Tuesday for demo
        this.autoSelectNextTuesday();
    }

    autoSelectNextTuesday() {
        const today = new Date();
        const nextTuesday = new Date(today);
        const daysUntilTuesday = (2 - today.getDay() + 7) % 7 || 7;
        nextTuesday.setDate(today.getDate() + daysUntilTuesday);
        
        // Select the Tuesday
        setTimeout(() => {
            this.selectDate(nextTuesday.getDate(), nextTuesday);
        }, 500);
    }

    selectDate(day, date) {
        // Remove previous selection
        this.calendarGrid.querySelectorAll('.calendar-day.selected').forEach(el => {
            el.classList.remove('selected');
        });
        
        // Select new date
        const dayElements = this.calendarGrid.querySelectorAll('.calendar-day.available');
        dayElements.forEach(el => {
            if (el.textContent == day) {
                el.classList.add('selected');
            }
        });
        
        this.selectedDate = date;
        document.getElementById('nextToTime').disabled = false;
    }

    generateTimeSlots() {
        const times = ['09:00', '10:00', '11:00', '13:00', '14:00', '15:00'];
        this.timeSlots.innerHTML = '';
        
        times.forEach(time => {
            const timeElement = document.createElement('div');
            timeElement.className = 'time-slot';
            timeElement.textContent = time;
            timeElement.addEventListener('click', () => this.selectTime(time));
            this.timeSlots.appendChild(timeElement);
        });
        
        // Auto-select 10:00 for demo
        setTimeout(() => {
            this.selectTime('10:00');
        }, 800);
    }

    selectTime(time) {
        // Remove previous selection
        this.timeSlots.querySelectorAll('.time-slot.selected').forEach(el => {
            el.classList.remove('selected');
        });
        
        // Select new time
        const timeElements = this.timeSlots.querySelectorAll('.time-slot');
        timeElements.forEach(el => {
            if (el.textContent === time) {
                el.classList.add('selected');
            }
        });
        
        this.selectedTime = time;
        document.getElementById('nextToForm').disabled = false;
    }

    nextStep() {
        if (this.currentStep >= 4) return;
        
        // Hide current step
        const currentStepEl = document.querySelector(`.booking-step[data-step="${this.currentStep}"]`);
        currentStepEl.classList.remove('active');
        
        // Show next step
        this.currentStep++;
        const nextStepEl = document.querySelector(`.booking-step[data-step="${this.currentStep}"]`);
        nextStepEl.classList.add('active');
        
        // Update progress
        this.updateProgress();
        
        // Auto-fill form for demo
        if (this.currentStep === 3) {
            setTimeout(() => this.autoFillForm(), 1000);
        }
        
        // Update summary for confirmation step
        if (this.currentStep === 4) {
            this.updateSummary();
        }
    }

    prevStep() {
        if (this.currentStep <= 1) return;
        
        // Hide current step
        const currentStepEl = document.querySelector(`.booking-step[data-step="${this.currentStep}"]`);
        currentStepEl.classList.remove('active');
        
        // Show previous step
        this.currentStep--;
        const prevStepEl = document.querySelector(`.booking-step[data-step="${this.currentStep}"]`);
        prevStepEl.classList.add('active');
        
        // Update progress
        this.updateProgress();
    }

    updateProgress() {
        const steps = document.querySelectorAll('.step');
        steps.forEach((step, index) => {
            const stepNumber = index + 1;
            if (stepNumber < this.currentStep) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (stepNumber === this.currentStep) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });
    }

    async autoFillForm() {
        const formData = {
            fullName: 'Erik Andersson',
            company: 'TechSoft AB',
            email: 'erik@techsoft.se',
            phone: '+46 70 123 45 67',
            message: 'Vi är intresserade av att implementera AI-chatbots för vår kundservice.'
        };
        
        for (const [fieldId, value] of Object.entries(formData)) {
            const field = document.getElementById(fieldId);
            if (field) {
                await this.typeIntoField(field, value);
                await this.delay(300);
            }
        }
        
        this.validateForm();
    }

    async typeIntoField(field, text) {
        field.value = '';
        field.focus();
        
        for (const char of text) {
            field.value += char;
            await this.delay(50);
        }
        
        field.blur();
    }

    validateForm() {
        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        
        const isValid = fullName && email && this.isValidEmail(email);
        document.getElementById('nextToConfirm').disabled = !isValid;
        
        return isValid;
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    updateSummary() {
        const dateStr = this.selectedDate.toLocaleDateString('sv-SE', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        document.getElementById('summaryDate').textContent = dateStr;
        document.getElementById('summaryTime').textContent = this.selectedTime;
        document.getElementById('summaryName').textContent = document.getElementById('fullName').value;
        document.getElementById('summaryEmail').textContent = document.getElementById('email').value;
    }

    async confirmBooking() {
        // Collect booking data
        this.bookingData = {
            date: this.selectedDate,
            time: this.selectedTime,
            name: document.getElementById('fullName').value,
            company: document.getElementById('company').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            message: document.getElementById('message').value
        };
        
        // Close modal
        this.closeBookingModal();
        
        // Show paper plane animation
        await this.delay(300);
        await this.showPaperPlaneAnimation();
        
        // Show success message
        await this.delay(3500);
        await this.showSuccessMessage();
        
        // Reset after success
        await this.delay(5000);
        await this.resetDemo();
    }

    async showPaperPlaneAnimation() {
        this.paperPlaneAnimation.classList.add('active');
        
        // Hide after animation completes
        setTimeout(() => {
            this.paperPlaneAnimation.classList.remove('active');
        }, 3000);
    }

    async showSuccessMessage() {
        this.successOverlay.classList.add('active');
        
        // Hide after delay
        setTimeout(() => {
            this.successOverlay.classList.remove('active');
        }, 4000);
    }

    async resetDemo() {
        // Reset all states
        this.currentStep = 1;
        this.selectedDate = null;
        this.selectedTime = null;
        this.bookingData = {};
        this.conversationStarted = false;
        
        // Clear chat messages
        const messages = this.chatMessages.querySelectorAll('.message');
        messages.forEach(msg => msg.remove());
        
        // Reset form
        this.contactForm.reset();
        
        // Reset modal steps
        document.querySelectorAll('.booking-step').forEach(step => {
            step.classList.remove('active');
        });
        document.querySelector('.booking-step[data-step="1"]').classList.add('active');
        
        // Reset progress
        this.updateProgress();
        
        // Close chat
        await this.closeChat();
        
        // Restart conversation after delay
        setTimeout(() => {
            this.startConversation();
        }, 3000);
    }

    changeMonth(direction) {
        // For demo purposes, we'll keep it simple and just regenerate current month
        this.generateCalendar();
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AxieChatbot();
});