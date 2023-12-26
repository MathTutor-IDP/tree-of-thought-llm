import re
import os
import pandas as pd
from src.tot.tasks.base import Task, DATA_PATH
from src.tot.prompts.math_reasoning import *
from src.tot.mathDataParser import DataParser


class MathTask(Task):
    """
    Input (x)   : a math problem
    Output (y)  : answer of the problem
    Reward (r)  : 0 or 1, depending on whether the answer is correct
    Input Example:
        Sixteen is 64$% of what number?
    Output Example:
        25
    """

    def __init__(self, file_path='data/'):
        super().__init__()
        self.mathDAO = DataParser(file_path)
        self.mathDAO.loadResults('level_5', 'algebra')
        self.value_cache = {}
        self.steps = 4
        self.stops = ['\n'] * 4
        self.gpt_usage = 0
        self.stop_iteration = False

    def __len__(self) -> int:
        return len(self.mathDAO)

    def get_input(self, idx: int) -> str:
        return self.mathDAO.questionsList[idx]

    @staticmethod
    def extract_answer(answer_raw):
        answer = answer_raw.replace(",", "")
        answer = [s for s in re.findall(r'-?\d+\.?\d*', answer)]
        if answer:
            return answer[0]
        return "Error:" + answer_raw

    def test_output(self, idx: int, output: str):
        expression = output.strip().split('\n')[-1].lower().replace('Final answer: ', '')
        model_answer = self.extract_answer(expression)
        correct_answer = self.extract_answer(self.mathDAO.resultsList[idx])
        try:
            model_answer = float(model_answer)
            correct_answer = float(correct_answer)
        except ValueError:
            pass

        if model_answer == correct_answer:
            return {'r': 1}
        else:
            return {'r': 0}

    @staticmethod
    def standard_prompt_wrap(question: str, y: str = '') -> str:
        return standard_prompt.format(question=question) + y

    @staticmethod
    def cot_prompt_wrap(question: str, y: str = '') -> str:
        return cot_prompt.format(question=question) + y

    def propose_prompt_wrap(self, question: str, y: str = '') -> str:
        if not y:
            return propose_first_step_prompt.format(question=question)
        elif "problem solved" in y.lower():
            self.stop_iteration = True
            return propose_final_step_prompt.format(question=question, solution=y)
        return propose_next_step_prompt.format(question=question, steps=y)

    @staticmethod
    def value_prompt_wrap(question: str, steps: str = '') -> str:

        if "final answer" not in steps[-1].lower():
            return value_prompt.format(question=question, steps=steps)
        return ''

    @staticmethod
    def value_outputs_unwrap(question: str, steps: str, value_outputs: list) -> float:
        if len(steps) == 4 and "final answer" not in steps[-1].lower():
            return 0

        value_names = [_.split('\n')[-1].replace('Evaluation: ', '') for _ in value_outputs]
        value_map = {'unlikely': 0.001, 'unsure': 1, 'likely': 20, 'solved': 9999}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value
