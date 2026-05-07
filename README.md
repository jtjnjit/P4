# Triv.io Game

## How To Run Locally
- Download zip file of all code
- Open in editor, such as VS Code
- Run the app using the command (py app.py)
- Then go to the localhost ip address given by Flask (shown in terminal)
- Explore the webpage

## Features
- Login / logout system that tracks user score and preferred settings through session cookies
- Create account feature that allows a user to have info saved in backend DB
- Backend database holds user info, high score, and date their account was created
- Contact page that sends an email to the backend DB
- Game setting page that stores a users settings
- Leaderboard which displays all high scores above 0
- Info removal page that allows users to request to be removed from the leaderboard

## In Progress
- Still need to create logic for a dynamic api call using the stored user game settings

contact = HTML DONE; Flask DONE
info-removal = HTML DONE; Flask DONE
create-acc = HTML DONE; Flask DONE
leaderboard = HTML DONE; Flask DONE (NEEDS CHECKED FOR OVERFLOW) (styling better) (top 3 colored) (make sure hover over row highlight works)
terms/priv statement = DONE
login = HTML Done; Flask DONE 
index = HTML toast style; Flask DONE
game settings = HTML DONE; Flask check over once done play-game
play-game = NONE; NONE