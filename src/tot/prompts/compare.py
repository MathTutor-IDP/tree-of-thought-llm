gpt_assistant_prompt = """Your task is compareing two given solutions from same question and find out if they are same or not. 
If the solutions are same, you should return 1, otherwise 0. 
Example1:
<solution1>\\frac{1}{2}</solution1> 
<solution2>Final answer: 5</solution2>
Answer:0

Example2:
<solution1>\\frac{1}{2}</solution1>
<solution2>Final answer: \\frac{2}{4}</solution2>

Answer:1

Example3:
<solution1>Final answer: \\frac{1}{2}</solution1>
<solution2>\\frac{3}{4}</solution2>
Answer:0

Example4:
<solution1>\\boxed{4}</solution1>
<solution2>Final answer: 20</solution2>
Answer:0


Example4:
<solution1>\\boxed{8}</solution1>
<solution2>Final answer: 8</solution2>
Answer:0
"""

gpt_question_prompt = """<solution1>{sol1}</solution1>
                         <solution2>{sol2}</solution2>"""
