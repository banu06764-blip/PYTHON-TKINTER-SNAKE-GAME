import tkinter
import random
root = tkinter.Tk()
root.geometry('1000x1000')
running = True
speed = 1000

def move():
    global running, speed
    if not running:
        return

    global direction, snake, pos
    headx, heady = pos[0]
    if direction == 'Right':
        new = (headx+20, heady)
    elif direction == 'Left':
        new = (headx-20, heady)
    elif direction == 'Up':
        new = (headx, heady-20)
    elif direction == 'Down':
        new = (headx, heady+20)

    pos[:] = [new] + pos[:-1]

    for i in range(len(snake)):
        canvas.coords(snake[i], pos[i][0], pos[i][1], pos[i][0]+20, pos[i][1]+20)

    collision()
    root.after(speed, move)

def Score():
    global score, speed
    score += 1
    label.configure(text=str(score))
    if speed > 100:
        speed = int(speed * 0.9)
    rand()

def rand():
    global treat, pos
    while True:
        x = random.randint(0, 780//20) * 20
        y = random.randint(0, 380//20) * 20
        if (x, y) not in pos:
            break
    treat = canvas.create_rectangle(x, y, x+20, y+20, fill='red')

def collision():
    global treat, snake, pos
    obj1_bbox = canvas.bbox(snake[0])
    obj2_bbox = canvas.bbox(treat)
    if obj1_bbox is None or obj2_bbox is None:
        return
    if (obj1_bbox[0] < obj2_bbox[2] and
        obj1_bbox[2] > obj2_bbox[0] and
        obj1_bbox[1] < obj2_bbox[3] and
        obj1_bbox[3] > obj2_bbox[1]):
        canvas.delete(treat)
        grow()
        Score()
    head = pos[0]
    if (head in pos[1:] or
        head[0] < 0 or head[0] >= 800 or
        head[1] < 0 or head[1] >= 600):
        gameover()

def gameover():
    global running
    running = False
    canvas.configure(bg='black')
    canvas.create_text(400, 300, text='gameover', fill='white')

def grow():
    global snake, pos
    tx, ty = pos[-1]
    snake.append(canvas.create_rectangle(tx, ty, tx+20, ty+20, fill='green1'))
    pos.append((tx, ty))

def check(event):
    global direction
    l = ['Left', 'Right', 'Up', 'Down']
    d = {'Left':'Right', 'Right':'Left', 'Up':'Down', 'Down':'Up'}
    if event.keysym in l and d[direction] != event.keysym:
        direction = event.keysym

tkinter.Label(root, text='score').pack()
label = tkinter.Label(root, text='0')
label.pack()
canvas = tkinter.Canvas(root, width=800, height=600, bg='yellow')
canvas.pack(anchor=tkinter.CENTER, expand=True)
direction = 'Left'
x = 370
y = 290
size = 20
score = 0
snake = [
    canvas.create_rectangle(x, y, x+size, y+size, fill='green'),
    canvas.create_rectangle(x+size, y, x+2*size, y+size, fill='green1'),
    canvas.create_rectangle(x+2*size, y, x+3*size, y+size, fill='green1')
]
pos = [(x, y), (x+size, y), (x+2*size, y)]
canvas.bind_all('<KeyPress>', check)

rand()
move()
root.mainloop()