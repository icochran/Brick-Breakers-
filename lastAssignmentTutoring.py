# Isabelle Cochran
# Brick breaking Game that is a work in progress but functional 

import turtle  # Using Turtle and Screen classes
import random  # Using randint

class Ball:
    """
    A class representing a ball on the screen
    """
    
    def __init__(self, t, radius, x, y, vx, vy, color):
        # Store the parameters in the new object atributes
        self.turtle = t
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = [vx, vy]
        self.color = color
               
    def update(self, rect, bricks):
        # Acquire the screen instance from the turtle
        screen = turtle.Screen()
        
        # Store current screen properties
        width = screen.window_width() 
        height = screen.window_height()
        masterList = []
        for i in bricks:
            if (i.isVisible):
                list = self.collide_with_rect(i)
                masterList.extend(self.collide_with_rect(i))
                if (len(list) > 0):
                    i.isVisible = False;
        
        if "t" in masterList:
            self.velocity[1] *= -1
        if "b" in masterList:
            self.velocity[1] *= -1
        if "l" in masterList:
            self.velocity[0] *= -1
        if "r" in masterList:
            self.velocity[0] *= -1
            
        list2 = self.collide_with_rect(rect)
        if "t" in list2:
            self.velocity[1] *= -1
                
        # Check for boundaries
        if (self.x - self.radius <= -width//2) or (self.x + self.radius >= width//2):
            self.velocity[0] *= -1
        if (self.y + self.radius >= height//2):
            self.velocity[1] *= -1
        
        # Update position with velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
    def collide_with_rect(self, rect):
        screen = turtle.Screen()
        height = screen.window_height()
        
        faces = []
        previousY = self.y - self.velocity[1]
        previousX = self.x - self.velocity[0]
        if (self.y - self.radius > -height//2): 
            if ((self.x + self.radius > rect.x and self.x - self.radius < rect.x + rect.w)):
                if (self.y - self.radius < rect.y < previousY - self.radius):
                    faces.append("t")
                if ((previousY + self.radius) < (rect.y - rect.h) < (self.y + self.radius) ):
                    faces.append("b")
            if ((self.y + self.radius) > (rect.y - rect.h) and (self.y - self.radius) < rect.y):
                if ((previousX + self.radius) < rect.x < (self.x + self.radius)):
                    faces.append("l")
                if (self.x - self.radius < (rect.x + rect.w) < previousX - self.radius):
                    faces.append("r")
        return faces

    def draw(self):
        """
        Draw the ball on the screen
        """
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.pendown()
        self.turtle.dot(self.radius * 2, self.color)
        
class Scene:
   
    def __init__(self):
        # Create a screen object (singleton) and set it up
        self.screen = turtle.Screen()
        self.screen.setup(0.5, 0.5)  # Use half with and half height of your current screen
        self.screen.tracer(False)
        self.screen.colormode(255)
        
        # Create an invisible turtle object
        self.turtle = turtle.Turtle(visible=False)
        
        # Initialize the scene
        self.initialize_objs()
    
        # Defines users' interactions we should listen for
        self.screen.onkey(self.done, 'q')  # Check if user pushed 'q'
        
        # As soon as the event loop is running, set up to call the self.run() method
        self.screen.ontimer(self.run, 0)
    
        # Tell the turtle screen to listen to the users' interactions
        self.screen.listen()
        
        # Start the event loop
        self.screen.mainloop()
        
    def initialize_objs(self):
        """
        Initializes the scene
        """
        # Defines the size of the game field       
        width = self.screen.window_width() - 20
        height = self.screen.window_height() - 20
        
        # Add ball to the game field with random location, velocity, and color        
        self.paddle = Paddle(self.turtle, 0, -height//2 + 20, 80, 10,
                             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.bricks = []
        brickW = width//10
        for i in range(10):
            self.bricks.append(Brick(self.turtle, -width//2 + brickW*i, height//2 - 20, brickW, 20, (random.randint(0, 255),               
                         random.randint(0, 255), random.randint(0, 255))))
        for j in range(10):
            self.bricks.append(Brick(self.turtle, -width//2 + brickW*j, height//2 - 40, brickW, 20, (random.randint(0, 255),               
                         random.randint(0, 255), random.randint(0, 255))))
        for k in range(10):
            self.bricks.append(Brick(self.turtle, -width//2 + brickW*k, height//2 - 60, brickW, 20, (random.randint(0, 255),               
                         random.randint(0, 255), random.randint(0, 255))))
            
        self.ball = Ball(self.turtle, 10, 0, 0, -2, -4, (random.randint(0, 255),
                                                         random.randint(0, 255), random.randint(0, 255)))
    def run(self):
        """
        Determines the game dynamic frame by frame (one frame for each call)
        """
        count = 0;
        # Clear the screen
        self.turtle.clear()
        height = self.screen.window_height() - 20
        for i in self.bricks:
            i.draw()
        for j in range(30):
            if not(self.bricks[j].isVisible):
                count += 1
        if (count == 30):
            self.turtle.clear()
            self.turtle.goto(0,0)
            self.turtle.write("Congratulations! You won the Game", False, "center", ("Arial", 24, "normal"))
        elif (self.ball.y - self.ball.radius > -height//2):
            self.paddle.update()
            self.paddle.draw()
            self.ball.update(self.paddle, self.bricks)
            self.ball.draw()
            # Update the overall screen
            self.screen.update()
        
            # Call the self.run() method 
            self.screen.ontimer(self.run, 0)
        
 
    def done(self):
        self.screen.bye()

class Paddle:
    
    def __init__(self, t, x, y, width, height, color):
        self.turtle = t
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color
        
    def draw(self):
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.pendown()
        self.turtle.fillcolor(self.color)
        self.turtle.begin_fill()
        self.turtle.forward(self.w)
        self.turtle.right(90)
        self.turtle.forward(self.h)
        self.turtle.right(90)
        self.turtle.forward(self.w)
        self.turtle.right(90)
        self.turtle.forward(self.h)
        self.turtle.right(90)
        self.turtle.end_fill()
        
    def update(self):
        self.x = turtle.getcanvas().winfo_pointerx() - 2*turtle.getcanvas().winfo_rootx() - self.w//2

class Brick:
    
    def __init__(self, t, x, y, width, height, color):
        self.isVisible = True;
        self.turtle = t
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.color = color
        
    def draw(self):
        if (self.isVisible):
            self.turtle.penup()
            self.turtle.goto(self.x, self.y)
            self.turtle.pendown()
            self.turtle.fillcolor(self.color)
            self.turtle.begin_fill()
            self.turtle.forward(self.w)
            self.turtle.right(90)
            self.turtle.forward(self.h)
            self.turtle.right(90)
            self.turtle.forward(self.w)
            self.turtle.right(90)
            self.turtle.forward(self.h)
            self.turtle.right(90)
            self.turtle.end_fill()
            
# Draw the scene
scene = Scene()

