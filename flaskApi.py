from flask import Flask, request, jsonify
from flask_cors import CORS
from someShitFunctions import display_board, check_termination, reset
import numpy as np
import copy
import json
from AgentSARSA import choose_action, reward, get_state

app = Flask(__name__)
CORS(app)
board = np.zeros((3, 3), dtype=int)
a = None
a_prev = None
board_prev = None
alpha = 0.5
gamma = 1
file_path = 'q_values.json'


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/setFile', methods=['POST'])
def set_file():
    global file_path
    data = request.json
    f = data.get('f')
    print( f )
    if f == 1:
        file_path = 'q_values.json'
    elif f == 2:
        file_path = 'q_values_new.json'
    if f == 1 or f == 2:
        return jsonify({"message": "Bot change recieved"}), 200
    else:
        return jsonify({"error": "wrong data sent"}), 400


@app.route('/api/logMove', methods=['POST'])
def receive_cell_data():
    # receives the move by the user from the frontend
    global board, a, a_prev, board_prev, file_path
    data = request.json
    row = data.get('row')
    col = data.get('col')
    move = data.get('move')
    if row == -1:
        board = reset(board)
        display_board(board)
        with open('q_values_new.json', 'w') as file:
            q = {"":""}
            json.dump(q, file, indent=4)
        return jsonify({"message": "kardiya reset bc", "termination": False}), 200
    tStatus = check_termination(board, (row, col), 1)
    board[row][col] = 1
    if check_termination(board) != -1:
        with open(file_path, 'r') as file:
            q_values = json.load(file)
        qValueA = q_values.get(str(a), 0.0)
        qValueA = qValueA + alpha * (reward(board) - qValueA)
        q_values[str(a)] = qValueA
        with open(file_path, 'w') as file:
            json.dump(q_values, file, indent=4)

    if row is not None and col is not None:
        print(f"Received data - Row: {row}, Column: {col}, Move:{move}")
        display_board(board)
        if tStatus != -1:
            board = reset(board)
            display_board(board)
            a = None
            a_prev = None
        return jsonify({"message": "Maal mil gaya guysssss", "termination": tStatus}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400


@app.route('/api/newMove', methods=['GET'])
def send_move():
    # sends the move by agent to the frontend
    global board, a, a_prev, board_prev, file_path
    move = choose_action(board, 0,file_path)
    row, col = move
    board[row][col] = 2
    a = get_state(board)

    if a_prev is not None:
        with open(file_path, 'r') as file:
            q_values = json.load(file)
        qValueA_prev = q_values.get(str(a_prev), 0.0)
        qValueA = q_values.get(str(a), 0.0)
        qValueA_prev = qValueA_prev + alpha * (reward(board_prev) + gamma * qValueA - qValueA_prev)
        q_values[str(a_prev)] = qValueA_prev
        with open(file_path, 'w') as file:
            json.dump(q_values, file, indent=4)
        if check_termination(board) != -1:
            with open(file_path, 'r') as file:
                q_values = json.load(file)
            qValueA = q_values.get(str(a), 0.0)
            qValueA = qValueA + alpha * (reward(board) - qValueA)
            q_values[str(a)] = qValueA
            with open(file_path, 'w') as file:
                json.dump(q_values, file, indent=4)

    board_prev = copy.deepcopy(board)
    a_prev = a
    display_board(board)
    tStatus = check_termination(board)

    response = jsonify({
        "row": row,
        "col": col,
        "termination": tStatus
    })

    print(response.data)
    if tStatus != -1:
        board = reset(board)
        display_board(board)
        a = None
        a_prev = None
    return response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
