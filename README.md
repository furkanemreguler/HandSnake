# 🐍 HandSnake

Control the classic Snake game using hand gestures! Move your hand in front of the camera to guide the snake - no keyboard needed.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-red.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)

## 🎮 Features

- **Hand Gesture Control**: Move your hand to control the snake's direction
- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand detection
- **Split Screen View**: Camera feed on the left, game on the right
- **Visual Feedback**: See gesture zones and detected directions in real-time
- **Classic Snake Gameplay**: Eat food, grow longer, avoid walls and yourself

## 🎯 How to Play

1. Position your hand in front of the camera
2. Move your hand in the direction you want the snake to go:
   - **Left**: Move hand to the left side
   - **Right**: Move hand to the right side
   - **Up**: Move hand upward
   - **Down**: Move hand downward
3. The snake will follow your hand movements!

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam
- Operating System: Windows, macOS, or Linux

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/furkanemreguler/HandSnake.git
cd HandSnake
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.8
pip install pygame==2.5.2
pip install numpy==1.24.3
```

## 🎮 Running the Game
```bash
cd src
python main.py
```

## ⌨️ Keyboard Controls

- **P**: Pause/Resume game
- **R**: Restart game
- **ESC**: Quit game
- **Arrow Keys**: Manual control (for testing)

## 📁 Project Structure
```
HandSnake/
├── README.md
├── requirements.txt
├── LICENSE
│
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main application
│   ├── snake_game.py           # Snake game logic
│   ├── gesture_controller.py  # Hand gesture detection
│   └── config.py               # Configuration settings
├── tests/
│   ├── __init__.py
│   ├── test_snake.py
│   └── test_gesture.py
│
└── examples/
    └── demo.py
```

## ⚙️ Configuration

Edit `src/config.py` to customize:

- **Screen size**: Change `SCREEN_WIDTH` and `SCREEN_HEIGHT`
- **Snake speed**: Adjust `SNAKE_SPEED`
- **Gesture sensitivity**: Modify `GESTURE_CONFIDENCE`
- **Colors**: Customize game colors
- **FPS**: Change frame rate

## 🎨 Gesture Zones

The camera feed shows colored zones to help you understand where to move your hand:

- **Blue zones** (left/right): Horizontal movement
- **Green zones** (up/down): Vertical movement
- **White crosshair**: Center reference point

## 🐛 Troubleshooting

### Camera not detected
```python
# In config.py, try changing CAMERA_INDEX
CAMERA_INDEX = 0  # Try 0, 1, or 2
```

### Hand not detected
- Ensure good lighting
- Keep hand within camera frame
- Try adjusting `GESTURE_CONFIDENCE` in config.py
- Make sure your hand is clearly visible against the background

### Game is too fast/slow
```python
# In config.py
SNAKE_SPEED = 10  # Lower = slower, Higher = faster
FPS = 30          # Frame rate
```

### Low FPS / Performance issues
- Close other applications
- Reduce screen resolution in config.py
- Update graphics drivers

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📚 Technologies Used

- **Python 3.8+**: Programming language
- **OpenCV**: Computer vision and camera handling
- **MediaPipe**: Hand tracking and gesture recognition
- **Pygame**: Game development and graphics
- **NumPy**: Array operations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Furkan Emre Guler**
- GitHub: [@furkanemreguler](https://github.com/furkanemreguler)

## 🌟 Acknowledgments

- MediaPipe team for the amazing hand tracking model
- Pygame community for game development support
- Classic Snake game for the inspiration



---

**Enjoy playing HandSnake! 🐍✋**
```
