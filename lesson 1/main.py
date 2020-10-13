import time
import curses
import asyncio
import random

TIC_TIMEOUT = 0.1

async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        delay = random.randint(1, 10)
        for i in range(delay):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(delay):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(delay):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(delay):
            await asyncio.sleep(0)

def draw(canvas):
    coroutines = []
    number_of_stars = 120
    maxy, maxx = canvas.getmaxyx()
    canvas.nodelay(True)
    for i in range(number_of_stars):
        symbol = random.choice('+*.:')
        row = random.randint(1, maxy - 2)
        column = random.randint(1, maxx - 1)
        coroutine = blink(canvas, row, column, symbol)
        coroutines.append(coroutine)

    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)

if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
