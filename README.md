# Axie Studio Chat Animation

A modern, animated chatbot interface for Axie Studio's booking system. Built with HTML, CSS, and JavaScript featuring smooth animations, realistic typing effects, and an interactive booking flow.

## Features

- **Modern UI Design**: Clean, professional interface with smooth animations
- **Realistic Chat Experience**: Typing indicators, message bubbles, and natural conversation flow
- **Interactive Booking System**: Multi-step booking process with calendar and time selection
- **Paper Plane Animation**: Beautiful confirmation animation after booking
- **Swedish Language Support**: Fully localized for Swedish users
- **Responsive Design**: Works seamlessly across all device sizes
- **Auto-Demo Mode**: Continuous demonstration loop for showcasing

## Demo Flow

1. **Welcome Message**: Bot greets the user and introduces Axie Studio
2. **Service Introduction**: Explains AI and chatbot solutions
3. **User Interest**: Simulated user shows interest in services
4. **Booking Offer**: Bot offers to schedule a demo
5. **Time Selection**: User expresses availability preference
6. **Booking Modal**: Interactive calendar and time slot selection
7. **Confirmation**: Paper plane animation and success message
8. **Loop Reset**: Automatically restarts for continuous demo

## Usage

### Quick Start
```bash
npm run dev
```
This will start a local server at `http://localhost:3000`

### Manual Setup
1. Clone the repository
2. Open `index.html` in a web browser
3. The chat animation will start automatically

## File Structure

```
├── index.html                 # Main HTML file
├── js/
│   └── chat-controller.js     # Main chat logic and animations
├── styles/
│   ├── chat-animations.css    # Chat interface and animation styles
│   └── main.css              # Global styles and variables
├── package.json              # Project configuration
└── README.md                 # This file
```

## Technologies

- **HTML5**: Semantic markup and structure
- **CSS3**: Modern animations, flexbox, grid, and custom properties
- **JavaScript (ES6+)**: Async/await, classes, and modern DOM manipulation
- **Node.js**: Development server (http-server)

## Key Features

### Chat Interface
- Smooth message animations with typing effects
- Realistic typing simulation for user messages
- Message fade-out system to maintain clean interface
- Responsive design for all screen sizes

### Booking System
- Multi-step modal with progress indicators
- Interactive calendar with date selection
- Time slot selection with visual feedback
- Booking confirmation with detailed summary

### Animations
- Paper plane flight animation after booking confirmation
- Success checkmark with bounce effect
- Smooth transitions between all states
- Highlight effects for user guidance

### Auto-Demo Mode
- Continuous loop for demonstration purposes
- Realistic timing between messages and actions
- Automatic booking flow simulation
- Clean reset between cycles

## Customization

### Colors
Edit CSS custom properties in `styles/chat-animations.css`:
```css
:root {
    --primary-color: #0066cc;
    --primary-light: rgba(0, 102, 204, 0.1);
    --text-color: #2c3e50;
    /* ... */
}
```

### Conversation Flow
Modify the `demoConversation` array in `js/chat-controller.js`:
```javascript
this.demoConversation = [
    { id: 'msg1', text: "Your message", isBot: true, delay: 1000 },
    // Add more messages...
];
```

### Timing
Adjust delays and animation speeds throughout the controller for different pacing.

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

MIT License - feel free to use this project for your own purposes.

## Contact

For questions about this demo or Axie Studio's services, visit [axiestudio.se](https://axiestudio.se)