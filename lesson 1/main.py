import time
import curses
import asyncio
import random

TIC_TIMEOUT = 0.1

async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed

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
    curses.curs_set(False)

    borders_size = 1
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - borders_size, columns - borders_size
    spaceship_rows = 20
    canvas_column_center = max_column // 2
    spaceship_row = max_row - spaceship_rows
    coroutines.append(fire(canvas, spaceship_row, canvas_column_center))

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
