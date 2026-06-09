# -*- coding: utf8 -*-
import csv
from abc import ABC, abstractmethod
from .task import Task
from .constraint import Constraint

__author__ = 'Mstislav Maslennikov'


class Solver(ABC):
    ''' Класс, задающий интерфейс для решателей задач.
        Интерфейс состоит из метода solve() и требуемых/несовместимых ограничений
    '''

    def __init__(self, task_path:str):
        ''' Инициализация

        :param constraints: ограничения
        '''
        self.task_path = task_path
        self.tasks = []
        self.constraints = []
        self.load()
        assert self.tasks, 'на вход решателя не поданы задачи'
        for task in self.tasks:
            assert isinstance(task, Task), 'задача не унаследована от Task'
        if self.constraints != []:
            for constraint in self.constraints:
                assert isinstance(constraint, Constraint), 'ограничение не унаследовано от Constraint'
        self.verify_constraints()

    def load(self):
        ''' Загрузить задачи и ограничения из файла input.csv '''
        self.tasks = []
        # Открываем файл для чтения
        with open(self.task_path, mode='r', encoding='utf-8') as file:
            # Используем DictReader, чтобы автоматически связать заголовки с данными
            reader = csv.DictReader(file)
            for row in reader:
                # Создаем объект Task, приводя все строки к int
                task = Task(
                    task_id=int(row['task_id']),
                    time=int(row['time']),
                    deadline=int(row['deadline']),
                    reward=int(row['reward'])
                )
                self.tasks.append(task)

    def verify_constraints(self):
        ''' Верификация статических ограничений

        :param tasks: задачи на входе
        :return:
        '''
        for constraint in self.constraints:
            if constraint.is_static():
                constraint.check(self.tasks)

    @abstractmethod
    def solve(self) -> list[int]:
        ''' Решить задачу

        :return: список номеров задач
        '''
        pass
