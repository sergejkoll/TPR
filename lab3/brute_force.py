import itertools
import math

import numpy as np


def brut_force(a, b, c, optimal_value):
    """
    Функция полного перебора всех возможных целочисленных переменных
    :param a: Уравнения системы ограничений
    :param b: Массив ограничений
    :param c: Функционал
    :param optimal_value: Результат симплекс метода
    :return: Оптимальное целочисленное решение
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    results = {}
    max_x = math.ceil(optimal_value / c[c > 0].min())

    for combination in itertools.product(np.arange(max_x), repeat=c.size):
        number_of_valid_constraints = 0
        for i in range(b.size):
            constraints = a[i] * combination
            if np.sum(constraints) <= b[i]:
                number_of_valid_constraints += 1

        if number_of_valid_constraints == b.size:
            result = np.sum(combination * c)
            results[result] = combination
            print(combination, result)

    return max(results.keys()), results[max(results.keys())]
