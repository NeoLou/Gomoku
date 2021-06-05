"Project Gomoku, by Neo Lou and Ryan Alizadeh"

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != " ":
                return False
    return True

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")



def is_bounded(board, y_end, x_end, length, d_y, d_x):

    first_is_empty = False
    last_is_empty = False
    f_x = x_end - length*d_x
    f_y = y_end - length*d_y
    l_x = x_end + d_x
    l_y = y_end + d_y
    if f_x in range(8) and f_y in range(8):
        first_is_empty = board[f_y][f_x] == " "
    if l_x in range(8) and l_y in range(8):
        last_is_empty = board[l_y][l_x] == " "
    ret_vals = ["CLOSED", "SEMIOPEN", "OPEN"]
    return ret_vals[first_is_empty + last_is_empty]


def test_is_bounded():
    board = make_empty_board(8)
    y = 1; x = 3; d_y = 1; d_x = -1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 1

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0

    y = y_start
    x = x_start

    col_switch = False

    if d_x == -1 and y == 0:
        d_to_border = max(y, x)

    else:
        d_to_border = 7 - max(y * d_y, x * d_x)

    for i in range(d_to_border):
        cur_y = y + i * d_y
        cur_x = x + i * d_x
        y_end = cur_y + (length - 1) * d_y
        x_end = cur_x + (length - 1) * d_x

        if board[cur_y][cur_x] == col and col_switch == False:

            actual_length = 0
            j = i
            while j < d_to_border + 1 and board[y + j * d_y][x + j * d_x] == col:
                actual_length += 1
                j += 1

            if actual_length == length:
                if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                    col_switch = True

                if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                    col_switch = True
            else:
                col_switch = True

        if board[cur_y][cur_x] != col:
            col_switch = False

    return open_seq_count, semi_open_seq_count

def test_detect_row():
    board = make_empty_board(8)
    #x = 5; y = 1; d_x = 0; d_y = 1; length = 2
    #put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    board[0][0] = "w"
    board[0][1] = "b"
    board[1][0] = "w"
    board[1][2] = "b"
    board[1][5] = "b"
    board[2][0] = "w"
    board[2][3] = "b"
    board[2][5] = "b"
    board[3][1] = "w"
    board[3][4] = "w"
    board[3][5] = "b"
    board[3][6] = "w"
    board[3][7] = "w"
    board[4][2] = "w"
    board[4][5] = "b"
    board[5][0] = "w"
    board[5][5] = "b"
    board[5][6] = "w"
    board[6][0] = "w"
    board[6][5] = "w"
    board[7][0] = "w"
    board[7][1] = "b"
    board[7][5] = "w"
    board[7][6] = "b"
    board[7][7] = "b"

    '''
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    '''

    print_board(board)

    col = "w"; length = 2; d_y = 1; d_x = -1; y = 4; x = 7

    if detect_row(board, col, y , x, length,d_y,d_x) == (1, -1):
        print("TEST CASE for detect_row PASSED")
    else:
        print(detect_row(board, col , y , x, length,d_y,d_x))
        print("TEST CASE for detect_row FAILED")

def detect_rows(board, col, length):

    open_seq_count, semi_open_seq_count = 0, 0


    for i in range(8):
        open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[1]

        open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[1]

        open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[0]
        open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[0]

        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[1]
        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[1]

    for l in range(1, 8):
        open_seq_count += detect_row(board, col, l, 0, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, l, 0, length, 1, 1)[1]

        open_seq_count += detect_row(board, col, l, 7, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, l, 7, length, 1, -1)[1]


    return open_seq_count, semi_open_seq_count

def does_row_win(board, col, end_y, end_x, d_y, d_x):
    """
    Assumes end_x, end_y is in board.
    Returns True iff the row of 5 defined by end_y, end_x, d_y, d_x is a win for colour col
    Returns False otherwise
    """
    if not (end_y - 4 * d_y in range(8) and end_x - 4 * d_x in range(8)):
        return False
    for i in range(5):
        if board[end_y - i*d_y][end_x - i*d_x] != col:
            return False
    if (end_y + d_y in range(8) and end_x + d_x in range(8)):
        if board[end_y + d_y][end_x + d_x] == col:
            return False
    if (end_y - 5 * d_y in range(8) and end_x - 5 * d_x in range(8)):
        if board[end_y - 5 * d_y][end_x - 5 * d_x] == col:
            return False
    return True

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'b'

    board[0][5] = "w"
    board[0][6] = "b"

    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)

    col = "w"; length = 3;

    if detect_rows(board, col,length) == (3,1):
        print(detect_rows(board, col,length))
        print("TEST CASE for detect_rows PASSED")
    else:
        print(detect_rows(board, col,length))
        print("TEST CASE for detect_rows FAILED")

def search_max(board):

    max_score = -100001
    optx = 0
    opty = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == " ":
                board[y][x] = "b"
                new_score = score(board)
                board[y][x] = " "
                #print(new_score)
                if new_score > max_score:
                    max_score = new_score
                    optx = x
                    opty = y
    return opty, optx

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):

    dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for y in range(8):
        for x in range(8):
            for direction in dirs:
                if does_row_win(board, "b", y, x, direction[0], direction[1]):
                    return "Black won"
                if does_row_win(board, "w", y, x, direction[0], direction[1]):
                    return "White won"

    count_empty = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == " ":
                count_empty += 1
    if count_empty == 0:
        return "Draw"
    return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))



def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        #analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res

        print("Your move:")
        move_y = int(input("Row: "))
        move_x = int(input("Column: "))
        while board[move_y][move_x] != " ":
            print("Square is already taken! Please choose an empty square.")
            move_y = int(input("Row: "))
            move_x = int(input("Column: "))
        board[move_y][move_x] = "w"
        print_board(board)
        #analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)


    board[0][5] = "w"
    board[0][6] = "b"


    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #


    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    play_gomoku(8)
