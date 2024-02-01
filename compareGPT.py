import os
import openai
import json
from src.tot.prompts.compare import gpt_assistant_prompt, gpt_question_prompt
import tqdm


class compareGPT:
    def __init__(self, log_path):
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key != "":
            openai.api_key = api_key
        else:
            raise Exception("OPENAI_API_KEY is not set")
        self.gpt_assistant_prompt = gpt_assistant_prompt
        with open(log_path) as file:
            self.__data = json.load(file)

    def send_request(self, solution1, solution2):
        prompt = gpt_question_prompt.format(sol1=solution1, sol2=solution2)
        message = [{"role": "assistant", "content": gpt_assistant_prompt},
                   {"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message,
            temperature=0.7,
            max_tokens=100
        )
        return response

    def parseResponse(self, response):
        responseStr = response["choices"][0]["message"]["content"]
        if "Answer:" in responseStr:
            return bool(int(responseStr[-1]))
        else:
            return responseStr

    def get_response(self, solution1, solution2):
        response = self.send_request(solution1, solution2)
        return self.parseResponse(response)

    def calculateDataAccuracy(self):
        acc = 0
        collector = []
        for question in tqdm.tqdm(self.__data):
            dataDict = {}
            calculated = question["steps"][-1]["final_result"]
            exact = question["infos"][0]["correct_answer"]
            dataDict["calculated"] = calculated
            dataDict["exact"] = exact
            dataDict["question"] = question["steps"][0]["x"]
            response = self.get_response(calculated, exact)
            dataDict["response"] = response
            collector.append(dataDict)
            if response:
                acc += 1
        with open("compare.json", "w") as file:
            json.dump(collector, file, indent=4)
        return dataDict, acc/len(self.__data)


if __name__ == "__main__":
    compare = compareGPT("geometry.json")
    _, acc = compare.calculateDataAccuracy()
    print(acc)
