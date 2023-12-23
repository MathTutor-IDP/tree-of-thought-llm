import os
import json
from typing import Any

DATA_MODES = ["test", "train"]
DATA_SUBTOPICS = ["algebra", "counting_and_probability", "geometry", "intermediate_algebra", "number_theory",
                  "prealgebra", "precalculus"]


class DataParser:
    def __init__(self, datapath) -> None:
        self.modes = DATA_MODES
        self.subtopics = DATA_SUBTOPICS
        self.datapath = datapath
        self.questionsList = []
        self.solutionList = []
        self.resultsList = []
        self.jsonlist = []
        self.results_dict = {}

    def __len__(self):
        return len(self.questionsList)

    def loadResults(self, mode: str, subtopic: str) -> None:
        self.questionsList = []
        self.solutionList = []
        self.resultsList = []
        self.jsonlist = []
        path_to_json = self.datapath + mode + "/" + subtopic + "/"

        # Get all the json file names in the selected directory
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

        for file_name in json_files:
            with open(path_to_json + file_name) as f:
                self.jsonlist.append(json.load(f))

        # Extract solutions to a list
        for data in self.jsonlist:
            self.questionsList.append(data["problem"])
            self.solutionList.append(data["solution"])

        # Extract results from the solutions
        for solution in self.solutionList:
            answer = self.findAnswer(solution)
            self.resultsList.append(answer)

        # Match results with the corresponding json
        for (fileid, result) in enumerate(self.resultsList):
            self.results_dict[fileid] = result

    def saveasfile(self, mode: str, subtopic: str) -> None:
        # Save results as json
        with open(self.datapath +"/" + mode + "/" + subtopic + '_answers.json', 'w') as fp:
            json.dump(self.resultsDict, fp)

    def findAnswer(self, solution: str) -> str:
        # Finds final answer from string using //boxed higlight in LaTeX.
        start = solution.rfind("boxed") + 6
        end = start + 1
        braketCounter = 0
        # Tries to find the end of //boxed{} area
        while end < len(solution) and (solution[end] != '}' or braketCounter != 0):
            if solution[end] == '{':
                braketCounter += 1
            if solution[end] == '}':
                braketCounter -= 1
            end += 1
            # Fail safe for misused boxed at the end
        if end == len(solution):
            return "ERROR"
        return solution[start:end]
