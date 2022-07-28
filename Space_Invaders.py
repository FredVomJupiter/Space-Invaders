# Space Invaders

import turtle
import math
import pygame

pygame.init()
game_over = pygame.mixer.Sound("C:/***(insert path to file here)***/gameover.wav")
explosion =pygame.mixer.Sound("C:/***(insert path to file here)***/explosion.wav")
fire = pygame.mixer.Sound("C:/***(insert path to file here)***/fire.wav")

# Setup window
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("black")
window.bgpic("C:/***(insert path to file here)***/background.gif")
window.tracer(0)

# Register shapes
window.register_shape("C:/***(insert path to file here)***/invader.gif")
window.register_shape("C:/***(insert path to file here)***/player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set a initial score
score = 0

# Draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("C:/***(insert path to file here)***/player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.speed = 0

# Choose number of invaders
number_of_invaders = 30

# Set speed of invaders
invader_speed = 0.2

# Create an empty list of invaders
invaders = []

# Add invaders to the list
for i in range(number_of_invaders):
    invaders.append(turtle.Turtle())

invader_start_x = -225
invader_start_y = 250
invader_number = 0

for invader in invaders:
    invader.color("red")
    invader.shape("C:/***(insert path to file here)***/invader.gif")
    invader.penup()
    invader.speed(0)
    x = invader_start_x + (50 * invader_number)
    y = invader_start_y
    invader.setposition(x, y)
    # Update the invader number
    invader_number += 1
    if invader_number == 10:
        invader_start_y -= 50
        invader_number = 0
    

# Create players weapon
weapon = turtle.Turtle()
weapon.color("yellow")
weapon.shape("triangle")
weapon.penup()
weapon.speed(0)
weapon.setheading(90)
weapon.shapesize(0.5, 0.5)
weapon.hideturtle()

weapon_speed = 7

# Weapon states
# Ready to fire
# Firing
weapon_state = "ready"

# Move player left and right
def move_left():
    player.speed = -1
    
def move_right():
    player.speed = 1

def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)

def fire_weapon():
    # Declare weapon state as global
    global weapon_state
    if weapon_state == "ready":
        weapon_state = "fire"
        # Play fire sound
        pygame.mixer.Sound.play(fire)
        # Move the weapon just above the player
        x = player.xcor()
        y = player.ycor() + 10
        weapon.setposition(x, y)
        weapon.showturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(), 2) + math.pow(t1.ycor()-t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False

# Create keyboard bindings
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(fire_weapon, "space")

# Play background music
pygame.mixer.music.load("invaders_music.wav")
pygame.mixer.music.play(-1)

# Game main loop
while True:

    window.update()
    move_player()

    for invader in invaders:
        # Move the invader
        x = invader.xcor()
        x += invader_speed
        invader.setx(x)

        # Reverse invaders direction when it reaches the boundaries
        if invader.xcor() > 280:
            # Nested loop that moves all the invaders down
            for i in invaders:
                y = i.ycor()
                y -= 40
                i.sety(y)
            # Changes direction only once and for all invaders
            invader_speed *= -1

        if invader.xcor() < -280:
            for i in invaders:
                y = i.ycor()
                y -= 40
                i.sety(y)
            invader_speed *= -1
    
        # Check if the weapon has hit the invader
        if isCollision(weapon, invader):
            # Play explosion sound
            pygame.mixer.Sound.play(explosion)
            # Reset the weapon if True
            weapon.hideturtle()
            weapon_state = "ready"
            weapon.setposition(0, -400)
            # Spawn a new invader on a random position
            invader.setposition(0, 10000)

            # Update score
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
        
        if isCollision(player, invader):
            # Play collision sound
            pygame.mixer.Sound.play(game_over)
            player.hideturtle()
            invader.hideturtle()
            print("Game Over")
            break

    # Move the weapon only if it has been fired
    if weapon_state == "fire":
        y = weapon.ycor()
        y += weapon_speed
        weapon.sety(y)

    # Check if the weapon reached the border
    if weapon.ycor() > 275:
        weapon.hideturtle()
        weapon_state = "ready"