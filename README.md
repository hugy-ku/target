# TARGET

## Project Description

- Project by: Hugh Jaiden
- Game Genre: Real-time Strategy

Game about capturing planets.

---

## Installation
To Clone this project:
```sh
git clone https://github.com/<username>/<project-name>.git
```

To create and run Python Environment for This project:

Window:
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Mac:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running Guide
After activate Python Environment of this project, you can process to run the game by:

Window:
```bat
python main.py
```

Mac:
```sh
python3 main.py
```

---

## Tutorial / Usage
Note: You can run main.py from any directory!
### Controls:
- WASD: Pan the camera
- Scroll wheel: Zoom the camera
- Space: Pause the game
- 1,2,3,4: Timescale (fast forward)
- Escape: Open menu
- Q and E: Secondary actions (indicated ingame if available)

You are the green planet. Drones spawn at a regular interval. Click on the planet to select it. Click on a connected planet to send all spawned Drones to the other planet. Right click to only send half instead. Dragging from a claimed planet to a connecting planet allows autosending.  
You capture the planet when the opposing planet reaches zero. When selecting a planet, you can upgrade the planet using the Q/E buttons. Factory increases the drone creation rate but is more fragile, and Fort defends twice as effectively against attacks.  
The Menu has four buttons: Resume, Restart, Statistics, and Exit. Resume resumes the game, restart starts a new game and creates a new map, statistics opens the statistics menu, and exit quits the game.  
Statistics menu shows the graph visualizations. Press Q/E to switch graphs. Press escape to stop viewing statistics.  
An AI is playing against you. I recommend pausing a lot!

---

## Game Features
- Visual representation in the scale of hundreds (aka Drones)!
- Fully implemented panning, zooming, pausing, fast-forwarding!
- Random map generation! Every game is different!
- Supports every frame rate and resolution!
- Enemy AI! (the non-generative kind)

---

## Known Bugs
- Planets getting captured twice in one tick in the same Route messes up the map unrecoverably. Use the Restart button in the menu.
- Map generation is a little wonky, routes may overlap and discerning which planets connect to which may be hard.
- Table in the statistics menu is not centered. Unfortunately row headers are not included in the centering calculation in matplotlib, so it is extremely hard to fix.
- AI does not account for drones on Routes.
- AI uses DFS when autosending when it should use BFS. (recursion does that)

---

## Unfinished Works
- TurretPlanet has been reduced in scale to FortPlanet.

---

## External sources
Thank you pygame-ce, numpy, pandas, and matplotlib developers for your hard work developing these libraries!