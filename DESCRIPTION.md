# Project Description

## 1. Project Overview
- **Project Name:**  
  Target
- **Brief Description:**  
  A 2D top-down real time strategy game about capturing planets. The game contains a map, consisting of circular planets and routes that connect them together. You start as the green faction, with one claimed planet. Claimed planets construct drones over time. These drones can be sent over to other planets through the routes to capture planets. Opposing drones destroy each other, whether on routes or defending their planet. If attackers win, the planet gets captured, otherwise, the defenders keep their planet. Planets have two mutually exclusive upgrades: Factories and forts. Factories produce double the drones, but their drones defend less effectively. Drones in forts defend twice as effectively, with no other downside. Upgrade cost varies between upgrades.
- **Problem Statement:**  
  The game this project is based on, Opacha-mda, refers to drones as power. They represent sending power through planets as a circle with a number in the middle. It was necessary to do this as it is limited in performance due to it being a mobile game, but this project doesn't have that kind of problem since it is meant to be run on a computer. I decided to turn power into drones, to turn it from "looking at numbers go up" to "looking at planets' orbits filling up with the might of a thousand* drones".  
  <small>*real game limits visible drones to 200 per planet for performance reasons</small>

- **Target Users:**  
  Anyone who reads the controls in README.md
  Or
  Anyone who likes games in general! The AI is a little hard but anyone can play!

- **Key Features:**  
  - Visual representation in the scale of hundreds (aka Drones)!
  - Fully implemented panning, zooming, pausing, fast-forwarding!
  - Random map generation! Every game is different!
  - Supports every frame rate and resolution!
  - Enemy AI! (the non-generative kind)

- **Screenshots:**
  - ![image_1](screenshots/gameplay/1.png)
  - ![image_2](screenshots/gameplay/2.png)
  - ![image_3](screenshots/gameplay/3.png)
  - ![image_4](screenshots/gameplay/4.png)
  - ![image_5](screenshots/gameplay/5.png)

- **Proposal**
  - [Proposal PDF](proposal.pdf)

- **Youtube Video**
  - [Video Link](https://youtu.be/n0I0MipqOL4)

## 2. Concept

### 2.1 Background
To be fully honest, *this is a learning experience.* The original game is already incredible, and the amount of polish put into far exceeds the current project. I based this project on the game because I played it a lot at the time, and I also had a working "drone orbiting system" I made on Scratch a few years back. I put arbitrary requirements on the game not because it's relevant to the proposal, but because I wanted to do it.

### 2.2 Objectives
- Create a game based on Opacha-mda for PC using Pygame, with statistical logging and graph visualization.
- Implement panning, zoom, pausing, and timescaling.
- Implement randomly generated planets and routes in a singular connected map, preferably one that looks good.
- Implement a system for transferring drones between planets and routes *visually*.
- 1 or more AI enemies for gameplay aspect.
- UI system for timescaling indication, upgrading, menu, and statistics
- 2 Upgrades with room for more implementations: Turret and Factory

Projet Objective: Be a learning experience.

## 3. UML Class Diagram
[UML Class Diagram Link](uml_diagram.pdf)

## 4. Object-Oriented Programming Implementation

### MainGame
- Stores the game display.
- Manages the mainloop and input handling.
- Source of tick() and render_tick().
- Communicates with Map, GameUi, and RenderManager and sends inputs to them.
- Stores and records statistics when the game ends.
- Manages the game state (timescaling, pausing, etc.).

### Map
- Stores planets, routes, and AI.
- Handles inputs to planets/routes.
- Random map generation happens here.
- Checks for when the game has ended also happens here.
- Also functions as an API for manipulating/accessing planets/routes.
- Ticks are passed on to planets, routes, and AIs. Statistical data is returned to MainGame.
- Render info from planets/routes are consolidated and passed to RenderManager.

### Planet
- Stores connected Routes in a list.
- Tick function creates drones and updates their target positions. Also returns the amount of drones created for statistics.
- get_drones calculates whether the incoming drones are friendly, if its getting captured, or if it successfully defends. If the drones are friendly, the amount of drones is added to the planet. If it is getting captured, replace itself by returning a new planet to Route which returns to Map. In addition, return the amount of drones destroyed for statistics as well.
- Can send drones to a connected route, called by Map.
- Render info is returned to Map for consolidation.

### UnclaimedPlanet, FactoryPlanet, FortPlanet
- Inherits from Planet.
- Changes Drone creation rate and vulnerability variable.
- Was intended to change functions for some planets (for example TurretPlanet may change render_info to add a turret head and change tick() to implement drone guns), but due to time constraints this was scrapped.

### Route
- Connects two planets together.
- Stores two planets (planet1 and planet2).
- Calculates number of ticks needed to travel between planets (AKA calculating weights).
- Stores drones currently travelling on the route.
- Tick is spaghetti code (sadly). moves all drones to their next positions. Once the drones travel to the end, remove from the stored list and call get_drones on the target planet. If opposing drones pass by each other, subtract them until only one group remains. Returns the replacement planet (if a planet gets captured) and number of destroyed drones to Map.
- Render info is returned to Map for consolidation.

### Drone
- Stores position, target position, and offset.
- Ticking moves the drone close to the target position, and offset is so all drones aren't the exact same.
- Offset is used for random orbit distance from the planet and location when on a Route.

### GameAi
- Access Map for information on the current state of the game.
- Stores color so it knows which planets they own.
- Many helper functions to simplify the tick() function.
- Tick controls AI behavior. Unclaimed planets are captured as soon as possible, safe planets are upgraded to factories (not used since the AI was determined to be too hard), planet in most danger requests all connected factories to autosend to it. Returns nothing since it is purely behavioral and does not affect rendering or statistics.

### RenderManager
- Manages the "viewport", a translation between the pixels on the monitor to coordinates on the game map.
- Manages the viewport's position and zoom, inputs are supplied from MainGame.
- Renders everything. Calls get_render_info() from GameUi and Map to get rendering data. All rendering data is organized into nested dictionaries and lists.

### GameUi
- manages the "UI rendering", which are usually texts, rects, and images. Includes timescale/pausing indicator, error alerts, buttons, and graphs.
- Manages Menu and StatisticsMenu
- Manages input for UI which can be passed on to Menu and StatisticsMenu.

### Menu
- Composed of 4 buttons.
- Toggled when user presses the escape key.
- Handles input for when buttons are pressed. Returns the button's name if one *is* pressed. MainGame handles the returned name.

### Button
- Stores a lot of attributes relating to rendering.
- Small function to check if mouse is clicked on the button.

### StatisticsMenu
- Self explanatory. Activated by pressing the "statistics" button in Menu.
- Formats the images generated by GraphGenerator into rendering data.
- Handles input for switching graphs.
- Calls GraphGenerator when switching to a new graph, and stores the newly made graph as a surface.

### GraphGenerator
- Imports pandas, numpy, matplotlib for creating graphs.
- Reads from statistics.csv and turns it into a table.
- Graphs are generated and saved as .png files in screenshots/visualization.
- Functions to switch graphs which returns file position for the graph.

## 5. Statistical Data

### 5.1 Data Recording Method
All data is recorded when game ends, from MainGame. Data is recorded to a statistics.csv in the same directory as main.py.

### 5.2 Data Features
- winner: Gotten from Map when it checks the game ending.
- gametime: Starts from 0 when game starts, delta time multiplied by timescale is added when the game is not paused. Resets to 0 when a new game starts.
- realtime: Same as gametime, but not affected by timescale and pausing (except for ui pausing like when in a menu).
- drones_created: Each tick, when planets create drones, the number of drones created are returned to Map, Map sums them all up and returns them to MainGame, and MainGame stores tem until the end of the game
- drones_destroyed: Same as drones_created, but taken from Route instead. Due to the design, Planets defending from attack returns the statistic to Route, and Route adds it with its own statistic from drones colliding en-route.
- factories, forts, unupgraded: Gotten from Map when it checks the game ending.

## 6. Changed Proposed Features
- As mentioned earlier, there would've been TurretPlanet which is both a visual upgrade and encourages more strategy. This was scrapped due to time constraints and the fact that "turret aim prediction" mentioned in the proposal means nothing as all drones are already heading directly to the planet.
- Not in the proposal, but there were plans to have a settings file and perhaps menu (that's why the UI was so extensible, if you look at renderManager.py and gameUi.py).

## 7. External Sources
Thank you pygame-ce, numpy, pandas, and matplotlib developers for your hard work developing these libraries!