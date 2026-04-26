import pyglet
from pyglet import window, shapes
from DIPPID import SensorUDP

PORT = 5700
sensor = SensorUDP(PORT)

SCALE = 3
WIDTH = 400 * SCALE
HEIGHT = 300 * SCALE

win = window.Window(WIDTH, HEIGHT, resizable=True)

@win.event
def on_resize(width, height):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height


score = 0
ball_active = False
acc_x = 0

batch = pyglet.graphics.Batch()

score_label = pyglet.text.Label(
    "Score: 0",
    font_size=25 * SCALE,
    x=WIDTH // 2,
    y=HEIGHT - 10,
    anchor_x='center',
    anchor_y='top',
    batch=batch
)

# Paddle
paddle = shapes.Rectangle(
    x=WIDTH // 2 - 60 * SCALE,
    y=50 * SCALE,
    width=120 * SCALE,
    height=15 * SCALE,
    color=(0, 200, 255),
    batch=batch
)

# Ball
ball = shapes.Circle(
    x=WIDTH // 2,
    y=120 * SCALE,
    radius=10 * SCALE,
    color=(255, 255, 255),
    batch=batch
)

ball_dx = 4 * SCALE
ball_dy = 4 * SCALE

# Farben für Wechsel
colors = [
    (0, 200, 255),
    (255, 100, 100),
    (100, 255, 100),
    (255, 255, 100),
    (255, 100, 255)
]
color_index = 0


def on_accel(data):
    global acc_x
    acc_x = float(data["x"])

def on_button(data):
    global ball_active
    if int(data) == 1:
        ball_active = True

sensor.register_callback("accelerometer", on_accel)
sensor.register_callback("button_1", on_button)


def update(dt):
    global ball_dx, ball_dy, ball_active, score, color_index

    # Paddle Movement
    paddle.x -= acc_x * 10 * SCALE

    # Clamp Paddle
    if paddle.x < 0:
        paddle.x = 0
    if paddle.x + paddle.width > WIDTH:
        paddle.x = WIDTH - paddle.width

    # Ball Movement
    if ball_active:
        ball.x += ball_dx
        ball.y += ball_dy

        # Seitenwände
        if ball.x <= 0:
            ball.x = ball.radius
            ball_dx *= -1

        if ball.x >= WIDTH:
            ball.x = WIDTH - ball.radius
            ball_dx *= -1

        # Decke
        if ball.y >= HEIGHT:
            ball.y = HEIGHT - ball.radius
            ball_dy *= -1


        # Boden
        if ball.y < 0:
            ball_active = False
            ball.x = WIDTH // 2
            ball.y = 120 * SCALE

            ball_dx = 4 * SCALE
            ball_dy = 4 * SCALE 
            
            score = 0
            score_label.text = "Score: 0"

        # Paddle Kollision
        if (
            paddle.x < ball.x < paddle.x + paddle.width and
            paddle.y < ball.y < paddle.y + paddle.height + 10 * SCALE
        ):
            ball.y = paddle.y + paddle.height + ball.radius
            ball_dy *= -1
            score += 1
            score_label.text = f"Score: {score}"

            # Farbe wechseln
            color_index = (color_index + 1) % len(colors)
            paddle.color = colors[color_index]
            ball.color = colors[color_index]

@win.event
def on_draw():
    pyglet.gl.glClearColor(0.05, 0.05, 0.1, 1)
    win.clear()
    batch.draw()
    score_label.x = WIDTH // 2
    score_label.y = HEIGHT - 10

pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()