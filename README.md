# Tic-Tac-Toe: Microservices Edition (Sketch Theme)

Welcome to the **Tic-Tac-Toe Microservices Project**! This project is a modern reimagining of the classic game, built with a robust Enterprise-grade architecture using **Spring Boot** microservices and a custom **Python (PyGame)** desktop client with a unique "Paper & Pencil" sketch aesthetic.

## 🌟 Features

### 🎮 Gameplay Modes
1.  **Single Player**: Challenge an AI with 5 difficulty levels.
    *   **Level 1**: Introduction (Random moves).
    *   **Level 3**: Competent (Blocks your winning moves).
    *   **Level 5**: Grandmaster (Impossible to beat - uses Minimax algorithm).
2.  **PVP (Hotseat)**: Play against a friend on the same computer.

### 🎨 Authentic Sketch UI
*   Unique hand-drawn visual style using procedural generation—no static images!
*   Every line, circle, and X is drawn slightly differently each time to simulate a real pencil on paper.
*   **Resolution Independent**: Scales perfectly from a small window up to **4K** resolution.

### 🏆 Global Leaderboard
*   Track scores across matches.
*   Wins grant **2 Points**.
*   Draws grant **1 Point**.
*   A centralized `leaderboard-service` maintains the rankings.

---

## 🏗️ Architecture & Technology Stack

This project uses a **Microservices Architecture** to ensure modularity and scalability.

### Backend (Spring Boot)
We split the logic into three distinct services, running independently:
1.  **Player Service** (`Running on Port 8081`):
    *   Manages player identities and nicknames.
    *   Database: H2 (In-Memory) for fast retrieval.
2.  **Leaderboard Service** (`Running on Port 8082`):
    *   Records match results and deals with scoring logic.
    *   Exposes APIs to get top players.
3.  **Game Service** (`Running on Port 8083`):
    *   Pure calculation engine.
    *   Stateless design (Input Board -> Output Move).
    *   Hosts the AI algorithms (Minimax).

### Frontend (Client)
*   **Python + PyGame**: Chosen for cross-platform compatibility (Windows/Linux) and performance.
*   **Custom UI Engine**: A modular `ui_core` was built from scratch to handle buttons, inputs, and the sketch rendering.

---

## 🧪 Unit Tests

We have written comprehensive Unit Tests to verify the integrity of each service.

### 1. Player Service Tests (`PlayerServiceTests.java`)
*   **`testCreatePlayer`**: Verifies that a new player can be registered via API.
*   **`testGetPlayer`**: Checks if we can retrieve an existing player's data.
*   **`testGetNonExistentPlayer`**: Ensures the system handles unknown users gracefully (404 Error).

### 2. Leaderboard Service Tests (`LeaderboardServiceTests.java`)
*   **`testSubmitScore`**: Verifies that points are correctly added to a player.
*   **`testLeaderboardOrder`**: **CRITICAL**. Ensures the API returns players sorted by highest score first.
*   **`testScoreUpdate`**: Checks that existing players get their scores *added* to, not overwritten.

### 3. Game Service Tests (`GameServiceTests.java`)
*   **`testMoveEndpoint`**: Basic health check for the AI move API.
*   **`testMinimaxBlock`**: Verifies AI Level 3 detects when you are about to win and blocks you.
*   **`testUnbeatableLevel`**: Verifies AI Level 5 calculates the perfect path to victory using Minimax.

---

## 🚀 How It Was Built (Layman's Guide)

Here is the journey of how we constructed this application:

1.  **Planning**: We started by defining the "Sketch" look and the Microservices requirement. We decided to separate the "Brain" (Java Backend) from the "Face" (Python Client).
2.  **Skeleton**: We created a "Parent" project to manage dependencies, then generated empty folders for each service.
3.  **Backend Construction**:
    *   We built `player-service` first to handle "Who is playing?".
    *   Then `leaderboard-service` to handle "Who is winning?".
    *   Finally `game-service` to handle "How do I play?". This is where the complex math for the AI lives.
4.  **Client Construction**:
    *   We didn't want boring grey buttons. We wrote a `SketchRenderer` that "jitters" lines to look like a hand drawing.
    *   We connected the Client to the Backend using **HTTP Requests** (like a web browser does). When you click a square, the Python app asks the Java app "Is this a win?" or "Where should the AI move?".
5.  **Quality Assurance**: We wrote the tests listed above to make sure no bugs slip in!

---

## 🏃 How to Run

### Prerequisite
*   **Java 17+** installed.
*   **Maven** installed (or use `./mvnw` if included).
*   **Python 3.x** installed.
*   Install Python libs: `pip install pygame requests`

### Step 1: Start the Backend
Open **3 separate Terminal windows** (one for each service) and run:

**Terminal 1 (Player Service)**:
```bash
cd c:/Users/SAMBANNER/Documents/GitHub/Tictactoe/player-service
mvn spring-boot:run
```

**Terminal 2 (Leaderboard Service)**:
```bash
cd c:/Users/SAMBANNER/Documents/GitHub/Tictactoe/leaderboard-service
mvn spring-boot:run
```

**Terminal 3 (Game Service)**:
```bash
cd c:/Users/SAMBANNER/Documents/GitHub/Tictactoe/game-service
mvn spring-boot:run
```

*Wait until you see "Started ...Application" in all three.*

### Step 2: Play the Game!
Open a **4th Terminal**:
```bash
cd c:/Users/SAMBANNER/Documents/GitHub/Tictactoe/tictactoe-client
python main.py
```

Enjoy your game!
