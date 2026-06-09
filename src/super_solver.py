# -*- coding: utf8 -*-
__author__ = 'Mstislav Maslennikov'

from .solver import Solver

__author__ = 'Mstislav Maslennikov'

class SuperSolver(Solver):
    ''' Класс для иллюстрации ограничений '''
    def __init__(self, tasks_path: str):
        super(SuperSolver, self).__init__(tasks_path)
        # проинициализировать SuperSolver, e.g. pulp/cvxopt/OR-Tools
        # использовать для этого ограничения

    def load(self):
        '''
        # разобрать файл с нестандартными ограничениями для этого типа солвера
        # например:
        [tasks]
        task_id, time, deadline, reward
        1, 1, 2, 1
        2, 5, 5, 2
        3, 1, 1, 2

        [task_precedence_constraints]
        task_1 < task_2
        task_3 < task_1

        [deadline_penalty]
        penalty: 0.3

        [target_constraints]
        target = reward - penalty
        '''

    def solve(self) -> list[int]:
        ''' Найти оптимальный порядок выполнения задач '''
        # запустить решатель SuperSolver
        # проверять во время запуска task_precedence_constraints, deadline_penalty, target_constraints
