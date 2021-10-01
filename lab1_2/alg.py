import numpy as np
import pandas as pd


def find_pivot(matrix):
    """
    Функция поиска разрешающего элемента
    :param matrix: симплекс таблица
    :return: координаты разрешающего элемента
    """
    j = np.argmax(matrix[-1:][0][1:]) + 1
    permissive_column = matrix[:, j]
    # permissive_column[permissive_column <= 0] = 0
    free_member_column = matrix[:, 0]
    with np.errstate(divide='ignore'):
        arr = free_member_column[:-1] / permissive_column[:-1]
        arr[arr <= 0] = np.inf
        i = arr.argmin()
        # i = np.where(free_member_column[:-1] > 0, free_member_column[:-1] / permissive_column[:-1], np.inf).argmin()
    return i, j


def swap(matrix, pivot, index, columns):
    """
    Функция замены базиса
    :param matrix: симплекс таблица
    :param pivot: разрешающий элемент
    :param index: первый столбец таблицы (содержит информацию о текущих переменных в базисе)
    :param columns: первая строка таблицы (содержит информацию о текущих свободных переменных)
    :return: таблица с новым базисом
    """
    index[pivot[0]], columns[pivot[1]] = columns[pivot[1]], index[pivot[0]]

    pivot_val = matrix[pivot]
    matrix_size = len(matrix[0])
    matrix_ = np.zeros((matrix_size, matrix_size))

    matrix_[pivot] = 1 / matrix[pivot]

    # разрещающая строка
    for j in range(matrix_size):
        if j == pivot[1]:
            continue
        matrix_[pivot[0], j] = matrix[pivot[0], j] / pivot_val

    # разрещающий столбец
    for i in range(matrix_size):
        if i == pivot[0]:
            continue
        matrix_[i, pivot[1]] = - matrix[i, pivot[1]] / pivot_val

    # остальные элементы симплекс таблицы, кроме разрешающих строки и столбца
    for i, j in [(i, j) for i in range(matrix_size) for j in range(matrix_size)]:
        if i == pivot[0] or j == pivot[1]:
            continue
        matrix_[i, j] = matrix[i, j] - matrix[pivot[0], j] * matrix[i, pivot[1]] / pivot_val

    return matrix_


def check_system(matrix):
    """
    Функция проверки наличия решения системы
    :param matrix: симплекс таблица
    :return:
    """
    for row in matrix:
        if row[0] < 0 and not np.any(row[1:] < 0):
            return False
    return True


def find_base_solution(matrix, index, columns):
    """
    Функция посика опороного решения
    :param matrix: симплекс таблица
    :param index: первый столбец таблицы (содержит информацию о текущих переменных в базисе)
    :param columns: первая строка таблицы (содержит информацию о текущих свободных переменных)
    :return: опорное решение
    """
    if not check_system(matrix):
        print("Система не имеет решений")
        return

    print("ПОИСК ОПОРНОГО РЕШЕНИЯ")
    while True:
        if not check_system(matrix):
            print("Система не имеет решений")
            return
        first_column = matrix[:-1, 0].flatten()
        negative_indices = np.where(first_column < 0, first_column, np.inf).argmin()
        if negative_indices == 0 and first_column[negative_indices] > 0:
            return matrix

        i = negative_indices
        row_i = matrix[i][1:]
        negative_index_in_row = np.where(row_i < 0, row_i, np.inf).argmin()
        j = negative_index_in_row
        j += 1
        base_column = matrix[:-1, j]
        # base_column[base_column <= 0] = 0
        with np.errstate(divide='ignore'):
            arr = first_column / base_column
            arr[arr <= 0] = np.inf
            i = arr.argmin()
            # i = np.where(first_column > 0, first_column / base_column, np.inf).argmin()
        print("_______________________________________________________________________________________________________")
        pivot = (i, j)
        print("Индекс разрешающего элемента: ", pivot)
        matrix = swap(matrix, pivot, index, columns)
        print(pd.DataFrame(data=matrix, index=index, columns=columns))


def find_optimal_solution(matrix, index, columns):
    """
    Функция поиска оптимального решения
    :param matrix: симплекс таблица
    :param index: первый столбец таблицы (содержит информацию о текущих переменных в базисе)
    :param columns: первая строка таблицы (содержит информацию о текущих свободных переменных)
    :return: симплекс таблицу с оптимальным решением
    """
    print("ПОИСК ОПТИМАЛЬНОГО РЕШЕНИЯ")
    while not all(i < 0 for i in matrix[-1][1:]):
        print("_______________________________________________________________________________________________________")
        pivot = find_pivot(matrix)
        print("Индекс разрешающего элемента: ", pivot)
        matrix = swap(matrix, pivot, index, columns)
        print(pd.DataFrame(data=matrix, index=index, columns=columns))

    print("_______________________________________________________________________________________________________")
    return matrix


def check_solution(origin_matrix, solution):
    f = 0
    for idx, item in enumerate(solution):
        if idx == 0:
            continue
        f += origin_matrix[-1][idx] * item
    assert solution[0] == -f, f"Результат оптимального решения не совпадает с коэффициентами F={solution[0]}, f={f}"

    for r, row in enumerate(origin_matrix[:-1]):
        multiplication = row[1:] * solution[1:]
        limit = np.sum(multiplication)
        assert row[0] >= limit, f"Ограничение №{r} нарушено: {limit} <= {row[0]}"
        print(f"Ограничение №{r}: {limit} <= {row[0]}")

    print("Решение верно!")


def run():
    c = np.array([8, 6, 2])
    A = np.array([
        [2, 1, 1],
        [1, 4, 0],
        [0, 0.5, 1]
    ])
    b = np.array([4, 3, 6])

    matrix = np.c_[b, A]
    matrix = np.r_[matrix, [[0, *c]]]
    origin_matrix = matrix

    s0 = "S0"
    columns = [s0] + [f'x{i+1}' for i in range(len(A[0]))]
    f = "F"
    index = [f'x{i+1+len(A[0])}' for i in range(len(A[:, 0]))] + [f]

    print(pd.DataFrame(data=matrix, index=index, columns=columns))

    matrix = find_base_solution(matrix, index, columns)
    matrix = find_optimal_solution(matrix, index, columns)
    answer = []
    for i, _ in enumerate(index):
        if f"x{i+1}" in index:
            answer.append(matrix[index.index(f"x{i+1}")][0])
        else:
            answer.append(0)

    print("x1 =", answer[0])
    print("x2 =", answer[1])
    print("x3 =", answer[2])
    print("F =", -matrix[3, 0])
    answer.insert(0, matrix[3, 0])

    check_solution(origin_matrix, answer[:-1])

    # Двойственная задача
    print("_________________ДВОЙСТВЕННАЯ ЗАДАЧА_________________")
    new_c = np.array(b) * -1
    new_b = np.array(c) * -1
    new_A = np.array(A.transpose()) * -1
    matrix_ = np.c_[new_b, new_A]
    matrix_ = np.r_[matrix_, [[0, *new_c]]]
    origin_matrix_ = matrix_

    index_ = ["y4", "y5", "y6", "F"]
    columns_ = ["S0", "y1", "y2", "y3"]
    print(pd.DataFrame(data=matrix_, index=index_, columns=columns_))

    matrix_ = find_base_solution(matrix_, index_, columns_)
    matrix_ = find_optimal_solution(matrix_, index_, columns_)
    answer_ = []
    for i, _ in enumerate(index_):
        if f"y{i+1}" in index_:
            answer_.append(matrix_[index_.index(f"y{i+1}")][0])
        else:
            answer_.append(0)

    print("y1 =", answer_[0])
    print("y2 =", answer_[1])
    print("y3 =", answer_[2])
    print("F =", matrix_[3, 0])
    answer_.insert(0, matrix_[3, 0])

    check_solution(origin_matrix_, answer_[:-1])
