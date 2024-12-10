import winsound#Used to play simple beep sounds for effects.
import random#Used to generate random values for enemy and ally movement or placement.
import turtle#Used for graphical rendering of the game
def distance(x1, y1, x2, y2):# It calculates the straight-line distance between two points x1,x2 y1,y2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
class Sprite(turtle.Turtle):#A class is a blueprint for creating objects in programming. It defines attributes (data) and methods (functions) that describe the behavior and properties of the objects.
    def __init__(self, spriteshape, color, startx, starty): #This line defines the constructor method __init__ for a class in Python. It initializes a new object's attributes when the object is created. __init__: Automatically called when an object is instantiated. self: Refers to the instance being created. Parameters (spriteshape, color, startx, starty): Inputs to initialize the object.
        super().__init__(shape=spriteshape)# Initialize a turtle with a custom shape.
        self.speed(0)# Maximize sprite animation speed.
        self.penup()#Tells the objects to stop drawing the line where it moving
        self.color(color) #Set sprite color.
        self.goto(startx, starty)#Move the sprite to its initial position.
        self.speed = 10#Default speed of sprite
    def move(self):# Moves the object forward by a certain distance, defined by the speed attribute of the object.
        self.forward(self.speed)# Move the sprite forward by its current speed
        if self.xcor()>290:  #If the x coordinate is greater than 290
            self.setx(290) #Set x coordinate is 290
            self.right(60) #Rotate 60 degree
        if self.xcor() < -290:#If the x coordinate is less than -290
            self.setx(-290)#Set x coordinate is -290
            self.right(60)#Rotate 60 degree
        if self.ycor() > 290:#If the y coordinate is greater than 290
            self.sety(290)#Set y coordinate is 290
            self.right(60)#Rotate 60 degree
        if self.ycor() < -290: #If the y coordinate is less than -290
            self.sety(-290)#Set y coordinate is -290
            self.right(60)#Rotate 60 degree
    def is_collision(self, other):#If objects collide into enemies it will lose
        return distance(self.xcor(), self.ycor(), other.xcor(), other.ycor()) < 20 #if x,y coordinates are less than 20 will be collide
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.speed = 8#Default Speed of moving play button
    def turn_left(self):#Define left function
        self.left(45)#Set for the object turn for 45 degree
    def turn_right(self):#Define right function
       self.right(45)#Set for the object turn for 45 degree
    def accelerate(self): #Speed up
        self.speed += 1
    def deaccelerate(self): #Speed down
        self.speed -= 1
class Enemy(Sprite):#Create enemy
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.speed = 6#Default speed of enemy
        self.setheading(random.randint(0, 360)) #Set the coordinates randomly from 0 to 360
class Ally(Sprite): #Create Ally
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.speed = 6#Default speed of ally
        self.setheading(random.randint(0, 360))#Set the coordinates randomly
    def move(self):
        super().move()#This calls the move() method of the parent class of the current class
        #which may have its own implementation of the move() method.
        #Boundary detection,when it touches the boundary the Ally will rotate right 60 degrees
        if self.xcor() > 290:#If the x coordinate greater than 290
            self.setx(290)  #Set Ally to x coordinate
            self.left(60)
        if self.xcor() < -290:#If the x coordinate less than -290
            self.setx(-290)  #Set Ally to x coordinate
            self.left(60)
        if self.ycor() > 290: #If the y greater than 290
            self.sety(290) #Set Ally to y coordinate
            self.left(60)
        if self.ycor() < -290:#If the y coordinate greater than 290
            self.sety(-290) #Set Ally to x coordinate
            self.left(60)
class Missile(Sprite): #Create missile
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None)#a missile should be smaller than planes and length>width with no outline
        self.speed = 20#Default speed of missle
        self.status = "ready"#This sets the status attribute of the object to "ready"
        self.goto(-1000, 1000)
        #This moves the missle to the coordinates (-1000, 1000)
        #These lines are used to reset the object's position and status. 
        #For example, when a missile is fired, it is moved off-screen and set to "ready" until the player fires it again. 
        #The missile will be repositioned on the screen when it is actually fired.
    def fire(self, player):
        if self.status == "ready":#This sets the status attribute of the object to "ready"
            self.goto(player.xcor(), player.ycor())#Related to user coordinates
            self.setheading(player.heading())# Match the player’s direction.
            winsound.Beep(1000, 20)#Sound 1000 is frequency, 20ms is period of the sound
            self.status = "firing"#change the status to "firing" the missile
    def move(self):#make a new move method for the missile, overwrite the Sprite move method
        if self.status == "ready":#if status== "ready"
            self.goto(-1000, 1000)#This moves the object to the coordinates (-1000, 1000)
        if self.status == "firing":#if status==firing
            self.forward(self.speed)#Move forward if firing with the same speed of object
            if abs(self.xcor()) > 290 or abs(self.ycor()) > 290:
                self.goto(-1000, 1000)
                self.status = "ready"
                 #This checks if the object has moved outside the boundary of the screen.
                 #If move outside the Missle is move to corner and not display to the user
                 #The object's status is set to "ready", indicating that the object is not in use and is ready for the next action
class Particle(Sprite):#Create enemy
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shape("circle")#Set shape to circle
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)#set shape size width=0.1, length=0.1, dooesnt have outline
        self.goto(-1000, -1000)#Move off the screen 
        self.frame = 0# used to initialize or reset the object’s state, especially in cases where the object has some form of animation or countdown.
    def explode(self, startx, starty):
        self.goto(startx, starty) #Move the sprite to its initial position
        self.setheading(random.randint(0, 360))#random from 0 to 360
        self.frame = 1#self.frame = 1 means that the object is now in the first step or phase of its action or animation
    def move(self):
        if self.frame > 0:# When it is greater than 0, the object moves forward by 10 units.
            self.forward(10)
            self.frame += 1#frame += 1 increases the frame value, indicating the animation is progressing.
        if self.frame > 20:#Once the frame exceeds 20, 
             #the object is reset (its frame is set to 0), and it is moved off-screen (goto(-1000, -1000)), indicating the end of its animation.
            self.frame = 0
            self.goto(-1000, -1000)
class Game():
    def __init__(self):
        self.level = 1#Start at level, will track current stage and track
        self.speed = 0#Game start at speed 0
        self.state = "playing"
        #sets the initial state of the game to "playing". 
        #The state could be used to track if the game is active, paused, or finished. The string "playing" suggests that the game is currently in progress.
        self.lives = 3  # Lives for the game, maximum 3
        self.score = 0#Start score=0
        # Border setup
        self.border_colors = ["red", "orange", "yellow", "green", "blue", "purple", "gray","violet"]#Define a list of colors that will be used to change the border's color in a cycle.
        self.border_color_index = 0#This initializes the index variable border_color_index, which keeps track of the current color in the self.border_colors list. The index starts at 0, meaning the first color (red) will be used initially. Just the first time install boader
        self.border = turtle.Turtle()#This creates a new turtle object named border. This turtle will be used to draw the border.
        self.border.speed(0)#This sets the boader drawing speed to 0, which means boarder will be draw as quickly as possible.
        self.border.pensize(5)#This sets the thickness of the lines drawn by the border turtle to 5 pixels.
        self.border.hideturtle()#This hides the turtle's cursor (the arrow) after it finishes drawing. It won't be visible during the animation process.
        # Pen setup
        self.pen = turtle.Turtle()#This creates a second turtle object named pen. This turtle won't be used for drawing borders but may be used for other purposes, like displaying text or status updates (in this case, the pen turtle is not used explicitly for drawing).
        self.pen.speed(0)#This sets the drawing speed of the pen turtle to the maximum value (0), so it won't slow down when drawing any status-related elements.
        self.pen.color("white")  # Set the pen color to white for visibility
        self.pen.penup()  # Lift the pen to avoid drawing lines
        self.pen.hideturtle()  # Hide the turtle cursor
        # Draw border and show initial status
        self.draw_border()
        self.show_status()
    # Draw border with current color
    def draw_border(self):
        self.border.penup()
        self.border.goto(-300, 300)
        self.border.pendown()#Start to draw
        for _ in range(4):#This starts a for loop that will run 4 times. The number 4 corresponds to the four sides of a square, as the turtle will move forward and turn right 90 degrees for each side.
            self.border.color(self.border_colors[self.border_color_index])#This line sets the color of the border turtle to the current color from the self.border_colors list. The current color is selected using self.border_color_index.
            self.border.forward(600)#This moves the border turtle forward by 600 units (a large enough distance to form the sides of the square).
            self.border.right(90)#After moving forward, this turns the border turtle 90 degrees to the right, which is necessary for drawing a square.
    # Update border color and redraw
    def update_border_color(self):
        self.border.clear()  # Clear the current border
        self.border_color_index = (self.border_color_index+1) % len(self.border_colors)#This increments the border_color_index and ensures that it wraps around to 0 after reaching the last color in the list. The % len(self.border_colors) part ensures the index stays within the range of valid indices for the self.border_colors list.
        self.draw_border()#This calls the draw_border() method again to draw the border with the new color.
        # Call this method again after 400ms
        turtle.ontimer(self.update_border_color, 400)
    # Show status, score, and lives
    def show_status(self):
        self.pen.clear()  # Clear previous text
        self.pen.goto(-280, 310)  # Position for score and lives display
        msg = f"Score: {self.score}  Lives: {self.lives}"#Write a string
        self.pen.write(msg, font=("Arial", 16, "bold"))  # Write the status
# Create game object
game = Game()
# Show the game status
game.show_status()
# Draw the initial border and start the color-changing animation
game.draw_border()
game.update_border_color()
# Initialize game
wn = turtle.Screen()
wn.bgcolor("black")  # Set initial background color
wn.title("SpaceWar")#Change window title box
wn.tracer(0)#Control how often the screen updates to improve performance, update screen every 0 step
# Create a list of background colors
background_colors = ["black", "darkblue","darkcyan"]#Create list with color for background
background_index = 0
# Function to update the background color
def update_background():
    global background_index#Inside update_background(), the global keyword is used to modify the background_index variable in the global scope.
    background_index = (background_index + 1) % len(background_colors)  # Cycle through colors
    wn.bgcolor(background_colors[background_index])  # Change the background color
    turtle.ontimer(update_background, 200)  # Change background every 200 miliseconds
# Start background color updates
update_background()
# Create game objects
player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)
enemies = [Enemy("circle", "red", random.randint(-250, 250), random.randint(-250, 250)) for _ in range(6)]
allies = [Ally("square", "blue", random.randint(-250, 250), random.randint(-250, 250)) for _ in range(9)]
particles = [Particle("circle", "orange", 0, 0) for _ in range(20)]#Make animation when fire
# Keyboard bindings
turtle.listen()
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.deaccelerate, "Down")
turtle.onkey(lambda: missile.fire(player), "space")#Here, we are passing a lambda function as the function argument. A lambda function is a small anonymous function that can be defined inline.
# Main game loop
def game_loop():
    if game.state == "playing":#The game's status is set to "playing", game is playing.
        player.move()#Make the object moving forward
        missile.move()#Make missile moving
        for enemy in enemies:# Move all enemies
            enemy.move()
            if player.is_collision(enemy):
                enemy.goto(random.randint(-250, 250), random.randint(-250, 250))
                game.lives -= 1 # Reduce lives by 1 on collision
                game.show_status()
            if missile.is_collision(enemy): #Check for collision between missile and the enemy
                enemy.goto(random.randint(-250, 250), random.randint(-250, 250))
                missile.status = "ready"#The missile's status is set to "ready", meaning the missile is no longer in flight and can be fired again later.
                game.score += 100 #Increase the score
                game.show_status()
                for particle in particles:
                   particle.explode(missile.xcor(), missile.ycor())#Do the explosion, when missle hit enemy
        for ally in allies:
            ally.move()
            if missile.is_collision(ally):
                ally.goto(random.randint(-250, 250), random.randint(-250, 250))
                missile.status = "ready"
                game.score -= 100
                game.show_status()
            if player.is_collision(ally):
                ally.goto(random.randint(-250, 250), random.randint(-250, 250))
                game.lives -= 1
                game.show_status()
        for particle in particles:
            particle.move()
        if game.lives <= 0:
            game.state = "game over"
            game.pen.goto(0, 0)
            game.pen.color("red")
            game.pen.write("Game Over", align="center", font=("Arial", 24, "bold"))
    wn.update()#Update realtime
    turtle.ontimer(game_loop, 20)#the game loop can run continuously and make the game interactive, with movements, collisions, and other updates happening regularly.
# Start the game
game_loop()
turtle.done()
#Classes allow us to bundle related data (attributes) and functions (methods) together.