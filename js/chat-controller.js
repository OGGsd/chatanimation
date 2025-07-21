class ChatController {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.querySelector('.send-button');
        this.typingIndicator = document.querySelector('.typing-indicator');
        this.isProcessing = false;
        this.isAnimating = false;
        this.processedMessages = new Set();
        this.maxVisibleMessages = 4;
        this.currentStep = 1;
        this.selectedDate = null;
        this.selectedTime = null;
        
        this.demoConversation = [
            { id: 'msg1', text: "Hej! Välkommen till Axie Studio! 👋", isBot: true, delay: 1000 },
            { id: 'msg2', text: "Vi hjälper företag med AI och chatbot-lösningar.", isBot: true, delay: 1500 },
            { id: 'msg3', text: "Hej! Jag är intresserad av era tjänster.", isBot: false, delay: 1200 },
            { id: 'msg4', text: "Vad bra! Jag kan hjälpa dig att boka en demo.", isBot: true, delay: 1500 },
            { id: 'msg5', text: "Det låter perfekt! När kan vi ses?", isBot: false, delay: 1000 },
            { id: 'msg6', text: "Vi har lediga tider nästa vecka. Passar tisdag eller onsdag?", isBot: true, delay: 1500 },
            { id: 'msg7', text: "Tisdag skulle fungera bra!", isBot: false, delay: 800 },
            { id: 'msg8', text: "Utmärkt! Jag öppnar bokningssystemet nu...", isBot: true, delay: 1200 },
            { id: 'msg9', text: "OPEN_BOOKING_MODAL", isBot: true, isSystem: true, delay: 500 }
        ];

        this.startDemo();
    }

    async startDemo() {
        while (true) {
            if (this.isAnimating) {
                await this.delay(1000);
                continue;
            }

            try {
                this.isAnimating = true;
                await this.runDemoCycle();
            } catch (error) {
                console.error('Error in demo cycle:', error);
                await this.delay(2000);
            } finally {
                this.isAnimating = false;
                await this.delay(3000); // Longer pause between cycles
            }
        }
    }

    async runDemoCycle() {
        // Reset everything
        this.processedMessages.clear();
        this.currentStep = 1;
        document.querySelector('.chat-container')?.classList.remove('fade-out');
        document.getElementById('modalContainer').innerHTML = '';
        document.getElementById('animationContainer').innerHTML = '';
        document.querySelector('.final-confirmation')?.remove();

        // Start fresh
        this.clearMessages();
        await this.animateInitialLoad();

        // Process messages
        for (const message of this.demoConversation) {
            if (message.isSystem) {
                await this.delay(message.delay);
                await this.openBookingModal();
                return;
            }

            if (message.isBot) {
                await this.showTypingIndicator();
                await this.delay(1500); // Longer typing delay
                await this.hideTypingIndicator();
                await this.addMessage(message);
            } else {
                await this.simulateUserTyping(message.text);
                await this.addMessage(message);
            }

            this.processedMessages.add(message.id);
            await this.delay(message.delay);
        }
    }

    async animateInitialLoad() {
        const container = document.querySelector('.chat-container');
        container.classList.add('active');
        await this.delay(800);
    }

    clearMessages() {
        this.chatMessages.innerHTML = '';
        this.typingIndicator = document.createElement('div');
        this.typingIndicator.className = 'typing-indicator';
        this.typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        this.chatMessages.appendChild(this.typingIndicator);
    }

    async addMessage(message) {
        if (this.processedMessages.has(message.id)) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.isBot ? 'bot-message' : 'user-message'}`;
        messageDiv.dataset.messageId = message.id;

        const contentSpan = document.createElement('span');
        messageDiv.appendChild(contentSpan);

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString('sv-SE', {
            hour: '2-digit',
            minute: '2-digit'
        });
        messageDiv.appendChild(timeDiv);

        this.chatMessages.insertBefore(messageDiv, this.chatMessages.firstChild);
        await this.typeText(contentSpan, message.text);
        this.manageVisibleMessages();
    }

    async typeText(element, text) {
        const words = text.split(' ');
        for (let i = 0; i < words.length; i++) {
            if (i > 0) element.textContent += ' ';
            const word = words[i];
            for (let char of word) {
                element.textContent += char;
                await this.delay(40); // Slightly slower typing
            }
            await this.delay(80); // Pause between words
        }
    }

    async simulateUserTyping(text) {
        if (this.isProcessing) return;
        this.isProcessing = true;

        try {
            this.messageInput.value = '';
            const words = text.split(' ');
            
            for (const word of words) {
                for (const char of word) {
                    this.messageInput.value += char;
                    await this.delay(60); // Realistic typing speed
                }
                this.messageInput.value += ' ';
                await this.delay(120); // Pause between words
            }
            
            this.sendButton.classList.add('active');
            await this.delay(300);
            this.sendButton.classList.remove('active');
            this.messageInput.value = '';
        } finally {
            this.isProcessing = false;
        }
    }

    async showTypingIndicator() {
        this.typingIndicator.classList.add('active');
        this.chatMessages.insertBefore(this.typingIndicator, this.chatMessages.firstChild);
    }

    async hideTypingIndicator() {
        this.typingIndicator.classList.remove('active');
    }

    manageVisibleMessages() {
        const messages = Array.from(this.chatMessages.getElementsByClassName('message'));
        messages.forEach((msg, index) => {
            if (index >= this.maxVisibleMessages) {
                msg.style.opacity = '0.2';
                msg.style.transform = 'translateY(-10px) scale(0.95)';
                msg.style.filter = 'blur(1px)';
            } else {
                const opacity = 1 - (index * 0.15);
                msg.style.opacity = opacity;
                if (index === this.maxVisibleMessages - 1) {
                    msg.classList.add('fading');
                }
            }
        });
    }

    async openBookingModal() {
        const modalContainer = document.getElementById('modalContainer');
        modalContainer.innerHTML = `
            <div class="booking-modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>Boka Din Demo</h2>
                        <div class="step-indicator">
                            <div class="step active">1. Välj Datum</div>
                            <div class="step">2. Välj Tid</div>
                            <div class="step">3. Bekräfta</div>
                        </div>
                    </div>
                    <div class="booking-content">
                        <div class="booking-step active" id="dateStep">
                            <div class="calendar-container">
                                ${this.generateCalendar()}
                            </div>
                            <button class="next-button" onclick="chatController.nextStep()">Nästa</button>
                        </div>

                        <div class="booking-step" id="timeStep">
                            <div class="time-slots">
                                ${this.generateTimeSlots()}
                            </div>
                            <div class="button-group">
                                <button class="back-button" onclick="chatController.prevStep()">Tillbaka</button>
                                <button class="next-button" onclick="chatController.nextStep()">Nästa</button>
                            </div>
                        </div>

                        <div class="booking-step" id="confirmStep">
                            <div class="booking-summary">
                                <h3>Bekräfta Din Bokning</h3>
                                <div class="summary-details">
                                    <div class="summary-item">
                                        <span class="label">Datum:</span>
                                        <span class="value" id="selectedDate">Tisdag, 14 Maj</span>
                                    </div>
                                    <div class="summary-item">
                                        <span class="label">Tid:</span>
                                        <span class="value" id="selectedTime">10:00</span>
                                    </div>
                                    <div class="summary-note">
                                        <p>Vi kommer att gå igenom:</p>
                                        <ul>
                                            <li>Era specifika behov och utmaningar</li>
                                            <li>Hur AI kan effektivisera er verksamhet</li>
                                            <li>Praktiska exempel och demonstrationer</li>
                                            <li>Kostnadsförslag och implementeringsplan</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div class="button-group">
                                <button class="back-button" onclick="chatController.prevStep()">Tillbaka</button>
                                <button class="confirm-button" onclick="chatController.handleBookingConfirmation()">Bekräfta Bokning</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Fade out chat interface
        const chatContainer = document.querySelector('.chat-container');
        chatContainer.classList.add('fade-out');

        // Show modal with animation
        const modal = modalContainer.querySelector('.booking-modal');
        await this.delay(10);
        modal.classList.add('show');

        // Auto-select date and time after a delay
        await this.delay(1500);
        await this.autoSelectDateTime();
    }

    generateCalendar() {
        const today = new Date();
        const nextTuesday = new Date(today);
        nextTuesday.setDate(today.getDate() + ((9 - today.getDay()) % 7));
        
        const monthName = nextTuesday.toLocaleString('sv-SE', { month: 'long' });
        const yearNum = nextTuesday.getFullYear();
        
        let calendarHtml = `
            <div class="calendar-header">
                <h3>${monthName} ${yearNum}</h3>
            </div>
            <div class="weekdays">
                <div>Mån</div>
                <div>Tis</div>
                <div>Ons</div>
                <div>Tor</div>
                <div>Fre</div>
                <div>Lör</div>
                <div>Sön</div>
            </div>
            <div class="calendar-grid" id="calendar">
        `;

        // Generate calendar days
        const monthStart = new Date(nextTuesday.getFullYear(), nextTuesday.getMonth(), 1);
        const monthEnd = new Date(nextTuesday.getFullYear(), nextTuesday.getMonth() + 1, 0);
        
        // Add empty cells for days before month starts
        const startDay = monthStart.getDay() === 0 ? 6 : monthStart.getDay() - 1;
        for (let i = 0; i < startDay; i++) {
            calendarHtml += '<div class="calendar-day empty"></div>';
        }

        // Add days
        for (let day = 1; day <= monthEnd.getDate(); day++) {
            const isSelected = day === nextTuesday.getDate();
            const isAvailable = day >= today.getDate();
            calendarHtml += `
                <div class="calendar-day ${isSelected ? 'selected' : ''} ${!isAvailable ? 'disabled' : ''}"
                     data-date="${day}"
                     onclick="chatController.selectDate(${day})">
                    ${day}
                </div>
            `;
        }

        calendarHtml += '</div>';
        return calendarHtml;
    }

    generateTimeSlots() {
        const times = ['09:00', '10:00', '11:00', '13:00', '14:00', '15:00'];
        return times.map((time, index) => `
            <button class="time-slot ${index === 1 ? 'selected' : ''}" onclick="chatController.selectTime('${time}')">
                ${time}
            </button>
        `).join('');
    }

    async autoSelectDateTime() {
        // Select date (14th)
        const dateCell = document.querySelector('.calendar-day.selected');
        if (dateCell) {
            dateCell.classList.add('highlight');
            await this.delay(800);
            dateCell.classList.remove('highlight');
            await this.delay(500);
            document.querySelector('#dateStep .next-button').click();
        }

        // Select time (10:00)
        await this.delay(1200);
        const selectedTimeSlot = document.querySelector('.time-slot.selected');
        if (selectedTimeSlot) {
            selectedTimeSlot.classList.add('highlight');
            await this.delay(800);
            selectedTimeSlot.classList.remove('highlight');
            await this.delay(500);
            document.querySelector('#timeStep .next-button').click();
        }

        // Confirm booking
        await this.delay(1500);
        const confirmButton = document.querySelector('.confirm-button');
        if (confirmButton) {
            confirmButton.classList.add('highlight');
            await this.delay(1000);
            confirmButton.classList.remove('highlight');
            await this.delay(300);
            confirmButton.click();
        }
    }

    selectDate(day) {
        const cells = document.querySelectorAll('.calendar-day');
        cells.forEach(cell => cell.classList.remove('selected'));
        const selectedCell = document.querySelector(`.calendar-day[data-date="${day}"]`);
        if (selectedCell) {
            selectedCell.classList.add('selected');
            this.selectedDate = day;
        }
    }

    selectTime(time) {
        const slots = document.querySelectorAll('.time-slot');
        slots.forEach(slot => slot.classList.remove('selected'));
        const selectedSlot = Array.from(slots).find(slot => slot.textContent.trim() === time);
        if (selectedSlot) {
            selectedSlot.classList.add('selected');
            this.selectedTime = time;
            document.getElementById('selectedTime').textContent = time;
        }
    }

    nextStep() {
        if (this.currentStep >= 3) return;
        
        const currentStepEl = document.querySelector(`.booking-step:nth-child(${this.currentStep})`);
        const nextStepEl = document.querySelector(`.booking-step:nth-child(${this.currentStep + 1})`);
        const stepIndicators = document.querySelectorAll('.step-indicator .step');
        
        currentStepEl.classList.remove('active');
        nextStepEl.classList.add('active');
        stepIndicators[this.currentStep].classList.add('active');
        
        this.currentStep++;
    }

    prevStep() {
        if (this.currentStep <= 1) return;
        
        const currentStepEl = document.querySelector(`.booking-step:nth-child(${this.currentStep})`);
        const prevStepEl = document.querySelector(`.booking-step:nth-child(${this.currentStep - 1})`);
        const stepIndicators = document.querySelectorAll('.step-indicator .step');
        
        currentStepEl.classList.remove('active');
        prevStepEl.classList.add('active');
        stepIndicators[this.currentStep - 1].classList.remove('active');
        
        this.currentStep--;
    }

    async handleBookingConfirmation() {
        // Hide the booking modal with fade
        const modalContainer = document.getElementById('modalContainer');
        const modal = modalContainer.querySelector('.booking-modal');
        modal.classList.remove('show');
        
        // Start paper plane animation
        await this.delay(500);
        await this.startPaperPlaneAnimation();
    }

    async startPaperPlaneAnimation() {
        const animationContainer = document.getElementById('animationContainer');
        animationContainer.innerHTML = `
            <div class="paper-plane-container">
                <div class="paper-plane">
                    <div class="plane-body"></div>
                    <div class="left-wing"></div>
                    <div class="right-wing"></div>
                </div>
                <div class="plane-trail"></div>
            </div>
        `;

        const planeContainer = animationContainer.querySelector('.paper-plane-container');
        await this.delay(100);
        planeContainer.classList.add('animate');
        
        await this.delay(4000); // Wait for plane animation to complete
        await this.showFinalConfirmation();
    }

    async showFinalConfirmation() {
        // Clear animation container
        document.getElementById('animationContainer').innerHTML = '';
        
        const container = document.createElement('div');
        container.className = 'final-confirmation';
        container.innerHTML = `
            <div class="confirmation-content">
                <div class="success-checkmark">✓</div>
                <h2>Bokning Bekräftad!</h2>
                <p>Vi ser fram emot att träffa er på tisdag kl 10:00</p>
                <div class="confirmation-details">
                    <p>En bekräftelse har skickats till din e-post med:</p>
                    <ul>
                        <li>Möteslänk för videosamtal</li>
                        <li>Agenda för demon</li>
                        <li>Förberedelsematerial</li>
                        <li>Kontaktinformation</li>
                    </ul>
                </div>
                <img src="https://www.axiestudio.se/logo.jpg" alt="Axie Studio Logo" class="confirmation-logo">
            </div>
        `;
        document.body.appendChild(container);

        await this.delay(100);
        container.classList.add('show');
        
        // Wait before starting next cycle
        await this.delay(6000);
        container.classList.remove('show');
        await this.delay(800);
        container.remove();
        
        // Reset chat container
        const chatContainer = document.querySelector('.chat-container');
        chatContainer.classList.remove('fade-out');
        
        // Clear modal container
        document.getElementById('modalContainer').innerHTML = '';
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize chat controller when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatController = new ChatController();
});