#リバーシの石の状態を示す定数
EMPTY, BLACK, WHITE, CAN_FLIP = 0, 1, 2, 3
STATUS = ["◻︎", "黒", "白", "・"]

#8方向の相対座標を示す定数[(dx,dy)...]
DIR_OFFSET = [(-1,-1), (-1, 0), (-1, 1),
              ( 0,-1),          ( 0, 1),
              ( 1,-1), ( 1, 0), ( 1, 1)]

#ボードを初期化する関数
def generate_board() -> list[list[int]]:
    board = [[EMPTY]*8 for _ in range(8)]
    board[3][4] = board[4][3] = BLACK
    board[3][3] = board[4][4] = WHITE
    return board

#(x,y)がボードの範囲内かどうかを調べる関数
def is_on_board(x: int, y: int) -> bool:
    return (0 <= x < 8) and (0 <= y < 8)

#白黒を反転する関数
def toggle(status: int) -> int:
    if status == EMPTY:
        return EMPTY
    return BLACK if status == WHITE else WHITE

#位置(x,y)の方向(dx,dy)に石を置けるかどうかを調べる
def can_flip_dir(board:list[list[int]], x:int, y:int, dx:int, dy:int, who:int) -> bool:
    if board[x][y] != EMPTY:#石がすでに置いてある
        return False
    if not is_on_board(x+dx, y+dy):#範囲外ならおけない
        return False
    if board[y+dy][x+dx] != toggle(who):#自分の石なら置けない
        return False
    #ひっくり返せるかどうか調べる
    for i in range(2,8):
        if not is_on_board(x + dx*i , y + dy*i):
            return False
        if board[y + dy*i][x + dx*i] == EMPTY:
            return False
        if board[y + dy*i][x + dx*i] == who:
            return True
    return False

#位置(x,y)に石を置けるか八つの方向を調べる
def can_flip(board:list[list[int]], x:int, y:int, who:int) -> bool:
    for dx, dy in DIR_OFFSET:
        if can_flip_dir(board, x, y, dx, dy, who):
            return True
    return False

#方向(dx,dy)に石を置く
def flip_dir(board:list[list[int]], x:int, y:int, dx:int, dy:int, who:int) -> int:
    if not can_flip_dir(board, x, y, dx, dy, who):
        return 0
    count = 0
    for i in range(1, 8):
        if not is_on_board(x + dx*i, y + dy*i):
            break
        if board[y + dy*i][x + dx*i] == who:
            break
        board[y + dy*i][x + dx*i] = who
        count += 1
    return count

#位置(x,y)に石を置く。ひっくり返した石の数を返す
def flip(board: list[list[int]], x:int, y:int, who:int) -> int:
    if not can_flip(board, x, y, who):
        return 0
    count = 0
    for dx, dy in DIR_OFFSET:
        count += flip_dir(board, x, y, dx, dy, who)
    board[y][x] = who
    return count

#石を置ける場所にマークを付ける関数
def add_flip_mark(board: list[list[int]], who:int) -> list[list[int]]:
    res = generate_board()
    for y in range(8):
        for x in range(8):
            res[y][x] = board[y][x]
            if board[y][x] == EMPTY:
                if can_flip(board, x, y, who):
                    res[y][x] = CAN_FLIP
    return res

#石の数を数える
def count_stone(board: list[list[int]], who:int ) -> int:
    return sum([ row.count(who) for row in board ])
def count_stone_both(board: list[list[int]]) -> tuple[int, int]:
    return count_stone(board, BLACK), count_stone(board, WHITE)

if __name__ == "__main__":
    l = generate_board()
    l = add_flip_mark(l, 2)
    m = [[" "*8] for _ in range(8)]
    for y in range(6):
        for x in range(6):
            if    l[y][x] == 1: m[y][x] = "●"
            elif  l[y][x] == 2: m[y][x] = "○"
            else: m[y][x] = "□"
    for i in l:
        print(i)
    for i in m:
        print(i)
    count = count_stone_both(l)
    print("Black_stone:", count[0])
    print("White_stone:", count[1])