
from snake.snake import Snake
from snake.food import Food
from snake.scoreboard import Scoreboard
from turtle import Screen, Turtle
import time


def play_snake():
    screen = Screen()
    screen.setup(width=600,height=600)
    screen.bgcolor("black")
    screen.title("My Snake Game")
    screen.tracer(0)

    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    screen.listen()
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")

    gameOver = False
    while not gameOver:
        screen.update()
        time.sleep(0.1)
        snake.move()

        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            scoreboard.increaseScore()

        if snake.head.xcor() > 300 or snake.head.xcor() < -300 or snake.head.ycor() > 300 or snake.head.ycor() < -300:
            gameOver = True
            scoreboard.endGame()

        for segment in snake.segments:
            for segment in snake.segments[1:]:
                if snake.head.distance(segment) < 10:
                    scoreboard.reset()
                    snake.reset()





    screen.exitonclick()