﻿# Lambda MUD

> Link to [Landing Page](https://lambdamud-game.netlify.com/)

> Link to [backend API](https://lambdamud-be.herokuapp.com/admin/)

## What is a MUD?

> A MUD...is a multiplayer real-time virtual world, usually text-based. MUDs combine elements of role-playing games, hack and slash, player versus player, interactive fiction, and online chat. Players can read or view descriptions of rooms, objects, other players, non-player characters, and actions performed in the virtual world. Players typically interact with each other and the world by typing commands that resemble a natural language. - Wikipedia

## Algorithm used to create the maze

> The algorithm used to create the maze was inspired by this [website](https://scipython.com/blog/making-a-maze/)

- The Depth-first search algorithm is a simple approach to generating a maze.
- The maze is consist of a grid of rooms; each room initially has four walls (North, East, South and East).
- Starting from the room at row=0 and column=0, we will aim to produce a path visiting each room according to the following procedure:

  - Inspect the neighboring rooms. If any of them have yet to be visited, pick one and move at random into it by removing the wall between them.

  - If no neighboring room is unvisited (a dead end), then backtrack to the last room with an unvisited neighbor.

  - In the implementation of this algorithm in the api (/api/make_maze), we use the Room model and build an entire maze. We wind our way through the grid of rooms at random, keeping track of the path we take on a stack implemented as a Python list. If we end up in a dead end, we simply pop visited rooms off the stack until we find one with unvisited neighbors.

## How to install the project?

### Download Project Files

- **Fork** and **Clone** this repository.
- **CD into the folder** where you cloned the repository.
- pipenv install to install all the necessary packages.
- manage.py makemigrations
- manage.py migrate
- ** Have to setup these environment variables**
- In production - Have to add the Postgres add-on to Heroku
- SECRET_KEY: a secret string
- DEBUG: False
- ALLOWED_HOSTS: .herokuapp.com, localhost, .netlify.com
- Pusher information: PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET, PUSHER_CLUSTER

## API Endpoints

### Auth Endpoints

| Method | Endpoint           | Description                                                                                                                                                                |
| ------ | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | /api/registration/ | Creates a `user` sent inside the `body` of the request in the form of {username, password1, password2}. Returns a key.                                                     |
| POST   | /api/              | Uses the credentials sent inside the `body` {username, password} to authenticate the user. On successful login, returns a token to be used to access restricted endpoints. |
| POST   | /api/make_maze/    | Uses the passed rows and columns numbers to generates a maze built with rooms. Returns a list containing the information for each room in the maze.                        |

### Adv endpoints

| Method | Endpoint       | Description                                                                                             |
| ------ | -------------- | ------------------------------------------------------------------------------------------------------- |
| GET    | /api/adv/init  | Initializes the player with the current user                                                            |
| GET    | /api/adv/reset | Reset the player's position to the first room                                                           |
| POST   | /api/adv/move  | Moves the player in the direction ('n', 's', 'w', 'e'). If the move is allowed, returns new coordinates |
| POST   | /api/adv/say   | Triggers a pusher request sending the passed message to all the players.                                |

## Data Models

### Room Data Model

| Field  | Type    | Description                                           |
| ------ | ------- | ----------------------------------------------------- |
| id     | Integer | ID of the newly created room.                         |
| user   | Integer | ID of the user in the room.                           |
| row    | Integer | Row number where the room is situated in the maze.    |
| column | Integer | Column number where the room is situated in the maze. |
| wall_n | Boolean | To signal if the room has a wall to the north         |
| wall_s | Boolean | To signal if the room has a wall to the south         |
| wall_e | Boolean | To signal if the room has a wall to the east          |
| wall_w | Boolean | To signal if the room has a wall to the west          |

### Player Data Model

| Field        | Type    | Description                             |
| ------------ | ------- | --------------------------------------- |
| id           | Integer | ID of the newly created room.           |
| user         | ID      | id of the current user.                 |
| current_room | Integer | id of the player's current room.        |
| uuid         | ID      | special id used to identify the player. |
