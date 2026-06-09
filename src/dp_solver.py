# -*- coding: utf8 -*-
import sys, csv
from .solver import Solver

__author__ = 'Mstislav Maslennikov'

class DPSolver(Solver):
    ''' Максимизирует суммарную награду задач, завершённых до дедлайна.  '''
    def __init__(self, tasks_path: str):
        super(DPSolver, self).__init__(tasks_path)

    def solve(self) -> list[int]:
        ''' Найти оптимальный порядок выполнения задач

        :param tasks:
        :return: идентификаторы задач в порядке выполнения
        '''

        # сортировка по дедлайнам, например:
        # Task3: t=1 d=1 r=2
        # Task1: t=1 d=2 r=1
        # Task2: t=5 d=5 r=2
        self.tasks.sort(key=lambda x: x.deadline)

        # dp[time] = максимальная награда, достижимая
        # для первых задач, имеющих суммарное время time
        dp = {0: (0, [])} # (награда, история задач + текущая задача)

        for task_id, task in enumerate(self.tasks, start=1):
            # копируем состояния без взятия задачи
            new_dp = dict(dp)
            # расширяем все состояния new_dp информацией о текущей задаче task_id
            for cur_time, (cur_reward, task_ids) in dp.items():
                new_time = cur_time + task.time
                if new_time > task.deadline:
                    # не добавляем, если дедлайн пропущен, так как награды не будет
                    continue
                new_reward = cur_reward + task.reward
                # обновление состояния
                if new_time not in new_dp or new_dp[new_time][0] < new_reward:
                    new_dp[new_time] = (new_reward, task_ids + [task.task_id])

            # удаляем задачи, для которых суммарное время больше, а награда не улучшается
            # используем эвристику лучшей награды для текущего времени
            new_dp_states = sorted(new_dp.items())
            pruned_dp = {}
            best_reward = -1
            for new_time, (new_reward, task_ids) in new_dp_states:
                if new_reward > best_reward:
                    pruned_dp[new_time] = (new_reward, task_ids)
                    best_reward = new_reward
            dp = pruned_dp

        # лучший результат
        best_time, (best_reward, task_ids) = max(dp.items(), key=lambda x: x[1][0])

        return task_ids


def main():
    if len(sys.argv) != 3:
        print('Usage: python dp_solver.py <input.csv> <output.csv>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    solver = DPSolver(input_path)
    task_ids = solver.solve()
    with open(output_path, 'w', newline='') as writer:
        writer = csv.writer(writer)
        writer.writerow(task_ids)

    print(f'Найдено решение, в котором {len(task_ids)} задач')
    print('Расписание: ' + ','.join(map(str, task_ids)))

if __name__ == '__main__':
    main()
