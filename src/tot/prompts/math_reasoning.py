standard_prompt = '''Solve the following math problem.

<Example>
Question: Let \\[f(x) = \\left\\{{\\n\\begin{{array}}{{cl}} ax+3, &\\text{{ if }}x>2, \\\\\\nx-5 &\\text{{ if }} -2 \\le x \\le 2, \\\\\\n2x-b &\\text{{ if }} x <-2.\\n\\end{{array}}\\n\\right.\\]Find $a+b$ if the piecewise function is continuous (which means that its graph can be drawn without lifting your pencil from the paper).
Answer: 0.
</Example>

<Task>
Question: {question}
Answer: 
</Task>
'''

cot_prompt = '''Solve the following math problem. Perform the solution by going step by step, and write down each step.

<Example>
Question: Let \\[f(x) = \\left\\{{\\n\\begin{{array}}{{cl}} ax+3, &\\text{{ if }}x>2, \\\\\\nx-5 &\\text{{ if }} -2 \\le x \\le 2, \\\\\\n2x-b &\\text{{ if }} x <-2.\\n\\end{{array}}\\n\\right.\\]Find $a+b$ if the piecewise function is continuous (which means that its graph can be drawn without lifting your pencil from the paper). Let's think step by step.
Solution: For the piecewise function to be continuous, the cases must "meet" at $2$ and $-2$. For example, $ax+3$ and $x-5$ must be equal when $x=2$. This implies $a(2)+3=2-5$, which we solve to get $2a=-6 \\Rightarrow a=-3$. Similarly, $x-5$ and $2x-b$ must be equal when $x=-2$. Substituting, we get $-2-5=2(-2)-b$, which implies $b=3$. So $a+b=-3+3=\\boxed{{0}}$.
</Example>

<Example>
Question: Sixteen is 64$\\%$ of what number? Let's think step by step.
Solution: If the number is $x$, we can set up the equation $\\frac{{16}}{{x}}=\\frac{{64}}{{100}}$. We divide both sides by $4$ to get $\\frac{{1}}{{x}}=\\frac{{4}}{{100}}=\\frac{{1}}{{25}}$, so $x=\\boxed{{25}}$.
</Example>

<Example>
Question: There are 3 complex numbers $a+bi$, $c+di$, and $e+fi$. If $b=1$, $e=-a-c$, and the sum of the numbers is $-i$, find $d+f$. Let's think step by step.
Solution: We know that $a+bi+c+di+e+fi=-i$. Thus, the real parts add up to 0 and the imaginary parts add up to -1. We then have  \\begin{{align}}\\na+c+e&=0\\\\\\nb+d+f&=-1\\\\\\n\\end{{align}}We know that $b=1$, therefore $d+f=\\boxed{{-2}}$
</Example>

<Task>
Question: {question} Let's think step by step.
Solution: 
</Task>
'''

propose_first_step_prompt = '''What would be a reasonable first step to solve the following math problem? Write down 3 different first steps. Do not write down the answer. Do not write down the question. Do not continue the solution. Do not write down the second step.
<Example>
Question: Let \\[f(x) = \\left\\{{\\n\\begin{{array}}{{cl}} ax+3, &\\text{{ if }}x>2, \\\\\\nx-5 &\\text{{ if }} -2 \\le x \\le 2, \\\\\\n2x-b &\\text{{ if }} x <-2.\\n\\end{{array}}\\n\\right.\\]Find $a+b$ if the piecewise function is continuous (which means that its graph can be drawn without lifting your pencil from the paper).
First step #1: For the piecewise function to be continuous, the cases must "meet" at $2$ and $-2$ which are the limits of f(x).
First step #2: $ax+3$ and $x-5$ must be equal when $x=2$. Also, $x-5$ and $2x-b$ must be equal when $x=-2$.
First step #3: Assume f(x) is continuous at $x=2$ and $x=-2$.
</Example>

<Example>
Question: Sixteen is 64$\\%$ of what number? 
First step #1: If the number is $x$, we can set up the equation $\\frac{{16}}{{x}}=\\frac{{64}}{{100}}$.
First step #2: Let $x$'s 64$\\%$ be 16. 
First step #3: Set up the equation $16=0.64x$.
</Example>

<Example>
Question: There are 3 complex numbers $a+bi$, $c+di$, and $e+fi$. If $b=1$, $e=-a-c$, and the sum of the numbers is $-i$, find $d+f$.
First step #1: We know that $a+bi+c+di+e+fi=-i$. Thus, the real parts add up to 0 and the imaginary parts add up to -1.
First step #2: Express the sum of the three complex numbers and equate it to $-i$.
First step #3: Separate the real and imaginary parts of the given condition.

</Example>

<Task>
Question: {question}
</Task>
'''

propose_next_step_prompt = '''Propose 3 alternatives that can be the next step to solve the following math problem.
If the solution is reached, write "Problem solved" at the end of the sentence. Give the response in three lines, not less, not more.
Each line should contain one alternative and 'Problem solved' statement at the end if the solution is reached.
Make sure that all alternative steps are coming right after the steps until now. Do not continue with the next steps of the ones that is just proposed.


<Example>
Question: Let \\[f(x) = \\left\\{{\\n\\begin{{array}}{{cl}} ax+3, &\\text{{ if }}x>2, \\\\\\nx-5 &\\text{{ if }} -2 \\le x \\le 2, \\\\\\n2x-b &\\text{{ if }} x <-2.\\n\\end{{array}}\\n\\right.\\]Find $a+b$ if the piecewise function is continuous (which means that its graph can be drawn without lifting your pencil from the paper).
Steps until now: For the piecewise function to be continuous, the cases must "meet" at $2$ and $-2$.
Next step alternative #1: For example, $ax+3$ and $x-5$ must be equal when $x=2$. This implies $a(2)+3=2-5$, which we solve to get $2a=-6 \\Rightarrow a=-3$.
Next step alternative #2: Set up the equation, $x-5$ and $2x-b$ must be equal when $x=-2$. Substituting, we get $-2-5=2(-2)-b$, which implies $b=3$.
Next step alternative #3: Therefore, $ax+3$=$x-5$ and $x-5$=$2x-b$ when $x=2$ and $x=-2$, respectively. This implies $a=-3$ and $b=3$, so $a+b=\\boxed{{0}}$. Problem solved.
</Example>

<Example>
Question: Sixteen is 64$\\%$ of what number? 
Steps until now: If the number is $x$, we can set up the equation $\\frac{{16}}{{x}}=\\frac{{64}}{{100}}$.
Next step alternative #1: We divide both sides by $4$ to get $\\frac{{1}}{{x}}=\\frac{{4}}{{100}}=\\frac{{1}}{{25}}$, so $x=\\boxed{{25}}$. Problem solved.
Next step alternative #2: We can cross multiply to get $16=0.64x$. Dividing both sides by $0.64$, we get $x=\\boxed{{25}}$. Problem solved.
Next step alternative #3: We can multiply both sides by $x$ to get $16=0.64x$. Dividing both sides by $0.64$, we get $x=\\boxed{{25}}$. Problem solved.
</Example>

<Example>
Question: There are 3 complex numbers $a+bi$, $c+di$, and $e+fi$. If $b=1$, $e=-a-c$, and the sum of the numbers is $-i$, find $d+f$.
Steps until now: We know that $a+bi+c+di+e+fi=-i$. Thus, the real parts add up to 0 and the imaginary parts add up to -1.
Next step alternative #1: We then have  \\begin{{align}}\\na+c+e&=0\\\\\\nb+d+f&=-1\\\\\\n\\end{{align}}We know that $b=1$, therefore $d+f=\\boxed{{-2}}$. Problem solved.
Next step alternative #2: We can set up the imaginary part equation $b+d+f=-1$. Since $b=1$, we get $d+f=-2$. Problem solved.
Next step alternative #3: Imaginary part of the equation becomes $b+d+f=-1$.
</Example>

<Task>
Question: {question}
Steps until now: {steps}

</Task>
'''

propose_final_step_prompt = ''' Extract the final answer given the question and solution steps.
<Example>
Question: Let \\[f(x) = \\left\\{{\\n\\begin{{array}}{{cl}} ax+3, &\\text{{ if }}x>2, \\\\\\nx-5 &\\text{{ if }} -2 \\le x \\le 2, \\\\\\n2x-b &\\text{{ if }} x <-2.\\n\\end{{array}}\\n\\right.\\]Find $a+b$ if the piecewise function is continuous (which means that its graph can be drawn without lifting your pencil from the paper). Let's think step by step.
Solution: For the piecewise function to be continuous, the cases must "meet" at $2$ and $-2$. For example, $ax+3$ and $x-5$ must be equal when $x=2$. This implies $a(2)+3=2-5$, which we solve to get $2a=-6 \\Rightarrow a=-3$. Similarly, $x-5$ and $2x-b$ must be equal when $x=-2$. Substituting, we get $-2-5=2(-2)-b$, which implies $b=3$. So $a+b=-3+3=\\boxed{{0}}$. Problem solved.
Final answer: 0
</Example>

<Example>
Question: Sixteen is 64$\\%$ of what number? Let's think step by step.
Solution: If the number is $x$, we can set up the equation $\\frac{{16}}{{x}}=\\frac{{64}}{{100}}$. We divide both sides by $4$ to get $\\frac{{1}}{{x}}=\\frac{{4}}{{100}}=\\frac{{1}}{{25}}$, so $x=\\boxed{{25}}$.  Problem solved.
Final answer: 25
</Example>

<Example>
Question: There are 3 complex numbers $a+bi$, $c+di$, and $e+fi$. If $b=1$, $e=-a-c$, and the sum of the numbers is $-i$, find $d+f$. Let's think step by step.
Solution: We know that $a+bi+c+di+e+fi=-i$. Thus, the real parts add up to 0 and the imaginary parts add up to -1. We then have  \\begin{{align}}\\na+c+e&=0\\\\\\nb+d+f&=-1\\\\\\n\\end{{align}}We know that $b=1$, therefore $d+f=\\boxed{{-2}}$. Problem solved.
Final answer: -2
</Example>

<Task>
Question: {question}
Solution: {solution}
Final answer: 
</Task>
'''

value_prompt = ''' Evaluate if given steps are likely to solve the question. Only mark as 'solved' if there is 'Problem Solved' in the steps. (solved, likely, unlikely, or unsure)
<Example>
Question: Let \\[f(x) = \\left\\{{\\n\\begin{{array}}{{cl}} ax+3, &\\text{{ if }}x>2, \\\\\\nx-5 &\\text{{ if }} -2 \\le x \\le 2, \\\\\\n2x-b &\\text{{ if }} x <-2.\\n\\end{{array}}\\n\\right.\\]Find $a+b$ if the piecewise function is continuous (which means that its graph can be drawn without lifting your pencil from the paper).
Steps: For the piecewise function to be continuous, the cases must "meet" at $2$ and $-2$.
Reasoning: criteria to make piecewise function is correct.
Evaluation: likely
</Example>

<Example>
Question: Sixteen is 64$\\%$ of what number? 
Steps: If the number is $x$, we can set up the equation $\\frac{{16}}{{x}}=\\frac{{64}}{{100}}$. We divide both sides by $4$ to get $\\frac{{1}}{{x}}=\\frac{{4}}{{100}}=\\frac{{1}}{{25}}$, so $x=\\boxed{{25}}$. Problem solved.
Reasoning: steps contains 'Problem solved' keyword
Evaluation: solved
</Example>

<Example>
Question: There are 3 complex numbers $a+bi$, $c+di$, and $e+fi$. If $b=1$, $e=-a-c$, and the sum of the numbers is $-i$, find $d+f$.
Steps:We know that $a+bi+c+di+e+fi=-i$. Thus, the real parts add up to 1 and the imaginary parts add up to 0.
Reasoning: equation is incorrect
Evaluation: unlikely
</Example>

<Task>
Question: {question}
Steps: {steps}
Reasoning: 
Evaluation: 
</Task>
'''



gpt_overuse_prompt = '''Solve the following math problem. Use the previous steps provided for the reasoning. Even if the given steps are not enough for the solution, you can use them to help you. Give the final answer as in the examples.

<Example>
Question: Let \\[f(x) = \\left\\{{\\n\\begin{{array}}{{cl}} ax+3, &\\text{{ if }}x>2, \\\\\\nx-5 &\\text{{ if }} -2 \\le x \\le 2, \\\\\\n2x-b &\\text{{ if }} x <-2.\\n\\end{{array}}\\n\\right.\\]Find $a+b$ if the piecewise function is continuous (which means that its graph can be drawn without lifting your pencil from the paper).
Steps: For the piecewise function to be continuous, the cases must "meet" at $2$ and $-2$. For example, $ax+3$ and $x-5$ must be equal when $x=2$. This implies $a(2)+3=2-5$, which we solve to get $2a=-6 \\Rightarrow a=-3$. Similarly, $x-5$ and $2x-b$ must be equal when $x=-2$. Substituting, we get $-2-5=2(-2)-b$, which implies $b=3$. So $a+b=-3+3=\\boxed{{0}}$.
Remaining steps: The solution has reached $a+b=\\boxed{{0}}$.
Final answer: 0
</Example>

<Example>
Question: Sixteen is 64$\\%$ of what number? Let's think step by step.
Steps: If the number is $x$, we can set up the equation $\\frac{{16}}{{x}}=\\frac{{64}}{{100}}$. We divide both sides by $4$ to get $\\frac{{1}}{{x}}=\\frac{{4}}{{100}}=\\frac{{1}}{{25}}$, so $x=\\boxed{{25}}$.
Remaining steps: The solution has reached $x=\\boxed{{25}}$.
Final answer: 25
</Example>

<Example>
Question: There are 3 complex numbers $a+bi$, $c+di$, and $e+fi$. If $b=1$, $e=-a-c$, and the sum of the numbers is $-i$, find $d+f$. Let's think step by step.
Steps: We know that $a+bi+c+di+e+fi=-i$. Thus, the real parts add up to 0 and the imaginary parts add up to -1.
Remaining steps: We then have  \\begin{{align}}\\na+c+e&=0\\\\\\nb+d+f&=-1\\\\\\n\\end{{align}}We know that $b=1$, therefore $d+f=\\boxed{{-2}}$
Final answer: -2
</Example>

<Task>
Question: {question}.
Steps: {steps}
Remaining steps: 
Final answer: 
</Task>
'''
