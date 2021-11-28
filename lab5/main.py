from game import Game

if __name__ == '__main__':
    # matrix = [[10, 11, 16, 15, 2],
    #           [9, 7, 6, 17, 1],
    #           [3, 0, 19, 15, 4],
    #           [0, 15, 13, 10, 6]]
    matrix = [[1, 3, 9, 6],
              [2, 6, 2, 3],
              [7, 2, 6, 5]]

    game = Game(matrix)
    result = game.solution()
    print("Оптимальная стратегия игрока А:")
    for idx, el in enumerate(result[0][1:]):
        print(f"x{idx+1} = {round(el, 3)}")
    print("\nОптимальная стратегия игрока B:")
    for idx, el in enumerate(result[1][1:]):
        print(f"y{idx+1} = {round(el, 3)}")
