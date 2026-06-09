# -*- coding: utf8 -*-
import os, csv, time, random
from .dp_solver import DPSolver
from unittest import TestCase

__author__ = 'Mstislav Maslennikov'

io_dir = os.path.dirname(__file__) + '/../io'


class TestDpSolver(TestCase):
    def test_solve_a0(self):
        ''' исходный тест, нужно выбрать [3, 1] '''
        input_path = os.path.join(io_dir, 'input.csv')
        output_path = os.path.join(io_dir, 'output.csv')

        # task_id,time,deadline,reward
        tasks = [
            [1, 1, 2, 1],
            [2, 5, 5, 2],
            [3, 1, 1, 2],
        ]

        # генерируем input.csv
        with open(input_path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(
                ['task_id', 'time', 'deadline', 'reward']
            )
            writer.writerows(tasks)

        # решаем задачу
        solver = DPSolver(input_path)
        task_ids = solver.solve()
        # генерируем output.csv
        with open(output_path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(task_ids)

        # проверяем решение
        self.assertEqual(task_ids, [3, 1])

    def _evaluate(self, tasks, task_ids):
        by_id = {row[0]: row for row in tasks}
        current_time = 0
        reward = 0

        for task_id in task_ids:
            _, duration, deadline, task_reward = by_id[task_id]
            current_time += duration
            if current_time <= deadline:
                reward += task_reward

        return reward

    def test_solve_random_300(self):
        ''' Нагрузочный тест:
        1. Решение не пустое.
        2. Все task_id уникальны.
        3. Все task_id существуют во входных данных.
        4. Полученная награда положительна.
        5. Решение выполняется за разумное время.
        '''
        rng = random.Random(42)
        input_path = os.path.join(io_dir, 'input_random_300.csv')
        output_path = os.path.join(io_dir, 'output_random_300.csv')
        tasks = []
        for task_id in range(1, 301):
            duration = rng.randint(1, 20)
            deadline = rng.randint(duration, 1000)
            reward = rng.randint(1, 100)
            tasks.append([task_id, duration, deadline, reward])

        with open(input_path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(['task_id', 'time', 'deadline', 'reward'])
            writer.writerows(tasks)

        started = time.perf_counter()
        solver = DPSolver(input_path)
        task_ids = solver.solve()
        elapsed = time.perf_counter() - started
        reward = self._evaluate(tasks, task_ids )

        # проверки
        self.assertGreater(len(task_ids), 0)
        self.assertEqual(len(task_ids),  len(set(task_ids)))

        all_task_ids = {row[0] for row in tasks}
        self.assertTrue(set(task_ids).issubset(all_task_ids))
        self.assertGreater(reward, 0)

        # для 300 задач должен работать быстро
        self.assertLess(elapsed, 10.0)

        print()
        print('==============================')
        print('DP SOLVER STRESS TEST')
        print('==============================')
        print(f'Tasks total      : {len(tasks)}')
        print(f'Tasks selected   : {len(task_ids)}')
        print(f'Total reward     : {reward}')
        print(f'Execution time   : {elapsed:.3f} sec')
        print()
        print('First 30 task ids:')
        print(task_ids[:30])
        print()

        with open(output_path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(task_ids)

    def test_solve_deadline_check(self):
        ''' Проверка дедлайна. Нельзя взять 1 + 2, потому что 3 + 3 = 6 > 4. Оптимум 2 + 3, награда 101'''
        input_path = os.path.join(io_dir, 'input_deadline.csv')
        output_path = os.path.join(io_dir, 'output_deadline.csv')

        rows = [
            [1, 3, 3, 10],
            [2, 3, 4, 100],
            [3, 1, 10, 1],
        ]
        expected = [2, 3]

        self.generate_input_csv(input_path, rows)
        solver = DPSolver(input_path)
        result = solver.solve()
        self.assertEqual(result, expected)

        with open(output_path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(result)

    def test_solve_reward_check(self):
        ''' Этот тест показывает, что нет лишнего отсечения (pruning), награда 59 '''
        input_path = os.path.join(io_dir, 'input_reward.csv')
        output_path = os.path.join(io_dir, 'output_reward.csv')

        rows = [
            [1, 2, 10, 5],
            [2, 2, 10, 50],
            [3, 2, 10, 4],
        ]
        expected = [1, 2, 3]

        self.generate_input_csv(input_path, rows)
        solver = DPSolver(input_path)
        result = solver.solve()
        self.assertEqual(result, expected)

        with open(output_path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(result)

    def test_solve_pruning_check(self):
        ''' Проверяет корректность отсечения (pruning). Возможны варианты: 1 + 3 = 9 или 2 = 9 '''
        input_path = os.path.join(io_dir, 'input_pruning.csv')
        output_path = os.path.join(io_dir, 'output_pruning.csv')

        rows = [
            [1, 4, 6, 8],
            [2, 5, 7, 9],
            [3, 1, 8, 1],
        ]
        expected = [2, 3]  # оптимальное решение с учётом pruning

        self.generate_input_csv(input_path, rows)
        solver = DPSolver(input_path)
        result = solver.solve()
        self.assertEqual(result, expected)

        with open(output_path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(result)

    def generate_input_csv(self, path, rows):
        with open(path, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(['task_id', 'time', 'deadline', 'reward'])
            writer.writerows(rows)