# -*- coding: utf8 -*-
import yaml
from pathlib import Path
from .task import Task
from abc import ABC, abstractmethod
from typing import Any

__author__ = 'Mstislav Maslennikov'

class Constraint(ABC):
    ''' Класс, задающий ограничения. Параметры ограничения могут быть статичными
    (до запуска решателя) и динамичными (проверяемыми в процессе решения '''

    constraints = None

    def __init__(self, type:str, static_params:dict[str, Any]):
        ''' При инициализации ограничения задаётся его тип и статичные параметры '''
        if not Constraint.constraints:
            current_dir = Path(__file__).resolve().parent
            Constraint.constraints = yaml.safe_load(current_dir/'constraints.txt')
        assert type in Constraint.constraints
        self.type = type
        self.static_params = static_params

    def is_static(self) -> bool:
        ''' Проверить, статичное ли ограничение '''
        return 'dynamic' not in Constraint.constraints[self.type]

    @abstractmethod
    def check(self, tasks:list[Task], **dynamic_params) -> Any:
        ''' Проверить ограничение

        :param tasks: список задач
        :param dynamic_params: динамические ограничения
        :return: результат ограничения, если нужно (как в примере с целевой функцией)
        '''
        pass


class TaskPrecedence(Constraint):
    ''' Ограничение с предшествующей задачей '''
    def check(self, tasks:list[Task], **dynamic_params) -> Any:
        if self.static_params['task_after'] == dynamic_params['task_id']:
            assert self.static_params['task_before'] in self.static_params['completed_tasks']


class DeadlinePenalty(Constraint):
    ''' Ограничение со штрафом за просрочку дедлайна '''
    def check(self, tasks:list[Task], **dynamic_params) -> Any:
        if dynamic_params['delay']:
            assert self.static_params['penalty'] < dynamic_params['reward']


class TargetFunction(Constraint):
    ''' Ограничение с целевой функцией '''
    def check(self, tasks: list[Task], **dynamic_params) -> Any:
        return dynamic_params['reward'] - dynamic_params['penalty']
