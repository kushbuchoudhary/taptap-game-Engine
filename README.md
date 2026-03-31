# 🎮 Game Hub - JSON-Configurable Game Engine

A sophisticated collection of 5 mini-games in a single application with **dynamic JSON-based configuration system**. Built with Python and Pygame, designed to showcase professional game development practices.

## 🎯 Games Included

1. **Flappy Bird** - Navigate through pipes avoiding obstacles. Score increases with each pipe passed.
2. **Arrow Shooter** - Shoot moving targets with arrows. Game ends after missing 3 times (miss_limit in JSON).
3. **Breakout** - Classic brick breaker. Move paddle to bounce ball and destroy bricks.
4. **Space Invaders** - Defend against alien invaders with simple classic rules. Game ends after 3 missed shots (no lives or bottom counters displayed).
5. **Snake** - Eat food to grow longer. Avoid walls and colliding with yourself.

## ⚙️ Dynamic Configuration System

The entire game engine is **configurable through JSON files** without touching any code:

### Difficulty Levels
- **Easy Mode** (`easy.json`) - Relaxed gameplay, higher tolerances, slower speeds
- **Medium Mode** (`medium.json`) - Balanced default difficulty
- **Hard Mode** (`hard.json`) - Challenging gameplay, faster speeds, stricter limits

### Configurable Parameters
All gameplay mechanics are externally defined:
- Physics (gravity, jump force)
- Speeds (player, bullet, enemy, pipes)
- Difficulty (arrow miss limit, space miss limit, brick counts, alien formations)
- Game dimensions and spawn rates

**Select difficulty level from menu before choosing a game - all selected game will use those parameters!**

## 🎮 Controls

### Menu
- Click **Difficulty Buttons** (Easy/Medium/Hard) to switch configurations
- Click **Game Buttons** to start playing

### In-Game Controls
- **Flappy Bird**: SPACE to jump
- **Arrow Shooter**: LEFT/RIGHT arrows to move, SPACE to shoot
- **Breakout**: LEFT/RIGHT arrows to move paddle
- **Space Invaders**: LEFT/RIGHT arrows to move, SPACE to shoot
- **Snake**: Arrow keys (↑↓←→) to change direction
- **All Games**: ESC or window close button to return to menu

## ✨ Key Features

- ✅ **JSON-Configurable Game Engine** - Change game behavior without code modifications
- ✅ **Multiple Difficulty Levels** - Easy, Medium, Hard modes for all games
- ✅ **Professional Architecture** - Clean separation of logic from configuration
- ✅ **Unified Hub Interface** - Seamlessly switch between 5 different games
- ✅ **Rapid Prototyping** - Test new game mechanics by editing JSON files
- ✅ **Extensible Design** - Easy to add new games and configurations

## 📁 File Structure

```
├── main.py                 # Game engine and hub
├── config.json            # Default (medium) configuration
├── easy.json              # Easy difficulty configuration
├── medium.json            # Medium difficulty configuration
├── hard.json              # Hard difficulty configuration
├── flappy.py              # Original Flappy Bird
├── game2.py, game3.py, etc. # Individual game files
└── README.md              # This file
```

## 🚀 How to Run

```bash
python main.py
```

1. Select a difficulty level (Easy/Medium/Hard)
2. Choose a game from the menu
3. Play the game!
4. Press ESC or close the window to return to menu

## 💡 How to Customize

### Create a New Difficulty Level
1. Copy `config.json` to `custom.json`
2. Modify game parameters as desired
3. In `main.py`, add a button calling `load_config("custom.json")`

### Modify Game Behavior
Simply edit the corresponding section in the JSON file:
```json
"flappy": {
  "physics": {"gravity": 0.5, "jump_force": -10},
  "pipes": {"speed": 4, "gap": 150}
}
```

Changes take effect immediately when you restart and select that difficulty level!

## 🎨 Why This Architecture Is Great

1. **Separation of Concerns** - Game logic and configuration are completely decoupled
2. **Non-Technical Customization** - Designers can adjust gameplay without touching code
3. **Rapid Prototyping** - Test design changes in seconds
4. **Professional Standard** - Matches modern AAA game development practices
5. **Scalability** - Easily add new games and configurations

## 📝 Technologies Used

- **Frontend**: Pygame (Python game library)
- **Core Language**: Python 3.x
- **Configuration**: JSON files
- **Libraries**: json, random, sys
