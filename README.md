**David’s Sleigh Dash** is a festive survival game where you pilot a holiday sleigh, dodging falling obstacles and collecting power-ups to stay alive. Coal pieces, big coal, and drifting snowflakes (during blizzards) threaten your sleigh, but you’ll have powerful items and events to help you push your survival time to the max!

## Features

1. **Movement**: Move left or right to dodge obstacles.  
2. **Three Lives System**: Each collision (unless shielded) reduces your lives by 1; the game ends at 0.  
3. **Power-Ups**:
   - **Speed Up (Red)**: Increases obstacle speeds for 10s.  
   - **Speed Down (Blue)**: Decreases obstacle speeds for 10s.  
   - **Shield (Gold)**: Negates collisions for 5s.  
   - **Freeze (Cyan)**: Stops obstacles for 7s.  
   - **Magnet (Gray)**: Pulls items toward you for 7s.  
   - **Health (Pink)**: Restores 1 life (up to max 3).  
   - **Event Trigger (Green)**: Randomly triggers **Blizzard** or **Meteor Shower**.  
4. **Special Events**:
   - **Blizzard (15s)**: Screen dims, snowflakes spawn, then removed after event ends.  
   - **Meteor Shower (15s)**: Obstacles speed up by a set amount, revert after 15s.  
5. **Adaptive Difficulty**: Big Coal appears after you survive 20s without losing a life, while meteor showers and blizzards keep you on your toes.

## Gameplay

- **Objective**: Survive as long as possible while collecting power-ups.  
- **Scoring**: The total time (in seconds) you remain in the game is your final score.  
- **Controls**: Use the left and right arrow keys to move your sleigh.  
- **End Screen**: Once you reach 0 lives, an end-screen shows your final score with a festive figure pointing at the result.

## Installation & Usage

1. **Clone or download** this repository.
2. Install Python (3.7+) and Pygame:
   ```bash
   pip install pygame
