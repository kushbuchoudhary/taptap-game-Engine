# 🎮 Flappy Bird Engine (JSON Controlled)

A custom Flappy Bird-style game built using Python and pygame, where the entire gameplay is controlled through an external JSON configuration file.

---

## 🚀 Key Idea

This project demonstrates a **mini game engine** where:

👉 Game behavior is NOT hardcoded  
👉 Everything is controlled using `config.json`  

This allows dynamic gameplay changes without modifying the code.

---

## ✨ Features

- 🐦 Flappy Bird mechanics (jump + gravity)
- 🧱 Dynamic pipe generation
- 💥 Collision detection (pipes, ground, ceiling)
- 🎯 Score system
- ⚙️ Fully JSON-controlled gameplay
- 🔄 Real-time behavior change via config
- 🖥️ Resizable game window

---

## 🧠 JSON-Based Control (Core Feature)

All important parameters are controlled using `config.json`:

```json
{
  "bird": {
    "jump_force": -9,
    "gravity": 0.35
  },
  "pipes": {
    "speed": 3,
    "gap": 180,
    "spawn_time": 1800
  },
  "game": {
    "screen_width": 600,
    "screen_height": 700
  }
}
