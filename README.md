
# 🌀 Emergency Evacuation Simulation using Agent-Based Modeling

This project simulates emergency evacuation dynamics using agent-based modeling and pheromone-inspired routing. It visualizes how agents (representing evacuees) navigate toward shelters while avoiding hazards and seeking hospitals, guided by evolving pheromone maps.

---

## 🔍 Features

- **Agent Movement**: Individuals move step-by-step based on pheromone intensity, environmental cues, and infrastructure proximity.
- **Pheromone Dynamics**: Agents deposit pheromones that diffuse and decay over time, influencing future movement.
- **Real-World Data Integration**: Supports CSV-based input for shelters, hospitals, transport hazards, and crowd density.
- **Infrastructure Mapping**: Visual overlays for shelters (🟢), hospitals (🔼), and hazards (❌).
- **Animated Output**: Generates labeled MP4/GIF showing evacuation progress with step count and active agent tracking.
- **Modular Design**: Easily extendable for panic modeling, urgency gradients, or multi-agent types.

---

## 📦 Tech Stack

| Component       | Tool/Library     |
|----------------|------------------|
| Language        | Python 3.10+     |
| Visualization   | Matplotlib       |
| Animation       | ImageIO          |
| Data Handling   | NumPy, Pandas    |
| Architecture    | Custom modules: `Agent`, `Environment`, `PheromoneMap`, `Simulation` |

---

## 📁 Data Inputs

Place your CSVs in a `/data` folder:

- `Shelter_Data.csv` – Shelter coordinates and scores  
- `Hospital_Data.csv` – Hospital locations and capacities  
- `Transport_Data.csv` – Hazard zones and penalties  
- `Warehouse_Data.csv` – Crowd density map

---

## 🚀 How to Run

```bash
python run.py
```

This will generate:

- `evacuation.mp4` – Animated simulation video  
- `evacuation.gif` – Optional GIF version (lower FPS)

---

## 📽️ Simulation Overview

- 🔵 Agents follow pheromone trails toward shelters  
- 🔴 Hazards repel agents and reduce pheromone strength  
- 🔼 Hospitals attract agents based on proximity and score  
- 🔥 Heatmap shows pheromone intensity  
- 📊 Overlays display step count and active agent count  
- 🧭 Legend explains all symbols

---

## 🧠 Extensions (Optional)

- Panic modeling (agents speed up near hazards)  
- Multi-agent types (elderly, injured, responders)  
- Real-time scoring and route optimization  
- Integration with GIS or real-time sensor feeds

---

## 📜 License

MIT License. Feel free to fork, extend, or adapt for research, hackathons, or deployment.

---


