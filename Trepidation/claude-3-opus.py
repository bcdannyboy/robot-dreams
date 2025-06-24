import math
import random
import time
import turtle

def setup():
    turtle.title("Trepidation")
    turtle.setup(800, 600)
    turtle.tracer(0)
    turtle.hideturtle()
    turtle.bgcolor("black")

def draw_anxious_lines(num_lines, color, thickness):
    for _ in range(num_lines):
        x = random.randint(-300, 300) 
        y = random.randint(-200, 200)
        length = random.randint(10, 100)
        heading = random.randint(0, 360)
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.pencolor(color)
        turtle.pensize(thickness)
        turtle.setheading(heading)
        turtle.forward(length)
        
def pulse_background(max_iter):
    r, g, b = 0, 0, 0
    for i in range(max_iter):
        turtle.bgcolor((r, g, b))
        r = (math.sin(i * 0.05) + 1) / 2
        g = (math.sin(i * 0.08) + 1) / 2 
        b = (math.sin(i * 0.13) + 1) / 2
        turtle.update()
        time.sleep(0.05)

def main():
    setup()
    
    while True:
        turtle.clear()
        pulse_background(200)
        draw_anxious_lines(50, "red", 2)
        draw_anxious_lines(30, "orange", 3) 
        draw_anxious_lines(10, "yellow", 5)
        turtle.update()

if __name__ == "__main__":
    main()