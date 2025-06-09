# Simple Flask web version of Gomoku
from flask import Flask, redirect, url_for, render_template_string
import random

from gomoku import create_board, check_five, computer_move, board_full

app = Flask(__name__)

board = create_board()
player = 1  # 1 is human, 2 is computer
message = ""

TEMPLATE = """
<!doctype html>
<title>Gomoku</title>
<h1>Gomoku Web</h1>
<p>{{ message }}</p>
<table border=1 cellpadding=5>
  {% for i,row in enumerate(board) %}
  <tr>
    {% for j,cell in enumerate(row) %}
    <td style="width:20px;height:20px;text-align:center">
      {% if cell == 0 %}
        <a href="{{ url_for('move', x=i, y=j) }}">.</a>
      {% elif cell == 1 %}X{% else %}O{% endif %}
    </td>
    {% endfor %}
  </tr>
  {% endfor %}
</table>
<p><a href="{{ url_for('reset') }}">Reset</a></p>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE, board=board, message=message)

@app.route('/move/<int:x>/<int:y>')
def move(x, y):
    global player, message
    if board[x][y] != 0:
        message = "Invalid move"
        return redirect(url_for('index'))

    board[x][y] = 1
    if check_five(board, 1):
        message = "You win!"
        return redirect(url_for('index'))
    if board_full(board):
        message = "Draw!"
        return redirect(url_for('index'))

    cx, cy = computer_move(board)
    board[cx][cy] = 2
    if check_five(board, 2):
        message = "Computer wins!"
    elif board_full(board):
        message = "Draw!"
    else:
        message = "Your move"
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global board, player, message
    board = create_board()
    player = 1
    message = "New game"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
