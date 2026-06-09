# -*- coding: utf8 -*-
from dataclasses import dataclass

__author__ = 'Mstislav Maslennikov'

@dataclass
class Task:
    ''' Класс, отвечающий за задачи, состоит из обязательных ограничений '''
    task_id: int  # Идентификатор задачи
    time: int  # Время выполнения tᵢ
    deadline: int  # Крайний срок выполнения dᵢ
    reward: int  # Награда за задачу, выполненную в срок (т.е. tstartᵢ+tᵢ <= dᵢ)
