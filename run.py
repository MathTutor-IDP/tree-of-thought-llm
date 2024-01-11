import os
import json
import argparse

from tot.tasks import get_task
from tot.methods.bfs import solve, naive_solve
from tot.models import gpt_usage

def run(args):
    task = get_task(args.task, args.split, args.category)
    logs, cnt_avg, cnt_any = [], 0, 0
    if args.naive_run:
        file = f'./logs/{args.task}/{args.backend}_{args.temperature}_naive_{args.prompt_sample}_sample_{args.n_generate_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    else:
        file = f'./logs/{args.task}/{args.backend}_{args.temperature}_{args.method_generate}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    os.makedirs(os.path.dirname(file), exist_ok=True)

    for i in range(args.task_start_index, args.task_end_index):

        info_init = {'idx': i}

        if hasattr(task, 'stop_iteration'):
            task.stop_iteration = False

        # solve
        if args.naive_run:
            ys, info = naive_solve(args, task, i) 
        else:
            ys, info , tree = solve(args, task, i)

        info_init.update(info)
        info = info_init
        # log
        infos = [task.test_output(i, y) for y in ys]
        info.update({'idx': i, 'ys': ys, 'infos': infos, 'usage_so_far': gpt_usage(args.backend)})
        logs.append(info)
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)
        if not args.naive_run:
            with open(f'./logs/{args.task}/{args.backend}_{args.temperature}_{args.method_generate}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}_tracking.json', 'a') as f:
                json.dump(tree, f, indent=4)
        
        # log main metric
        accs = [info['r'] for info in infos]
        cnt_avg += sum(accs) / len(accs)
        cnt_any += any(accs)
        print(i, 'sum(accs)', sum(accs), 'cnt_avg', cnt_avg, 'cnt_any', cnt_any, '\n')
    
    n = args.task_end_index - args.task_start_index
    print(cnt_avg / n, cnt_any / n)
    print('usage_so_far', gpt_usage(args.backend))


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--backend', type=str, choices=['gpt-4', 'gpt-3.5-turbo'], default='gpt-3.5-turbo')
    args.add_argument('--limit', type=int, default=20)
    args.add_argument('--temperature', type=float, default=0.7)

    args.add_argument('--task', type=str, required=False, choices=['game24', 'text', 'crosswords', 'math'],default='math')
    args.add_argument('--task_start_index', type=int, default=2)
    args.add_argument('--task_end_index', type=int, default=56)

    args.add_argument('--naive_run', action='store_true')
    args.add_argument('--prompt_sample', type=str, choices=['standard', 'cot'],default="cot")  # only used when method_generate = sample, or naive_run

    args.add_argument('--method_generate', type=str, choices=['sample', 'propose'],default="sample")
    args.add_argument('--method_evaluate', type=str, choices=['value', 'vote'], default='value')
    args.add_argument('--method_select', type=str, choices=['sample', 'greedy'], default='greedy')
    args.add_argument('--n_generate_sample', type=int, default=5)  # only thing needed if naive_run
    args.add_argument('--n_evaluate_sample', type=int, default=1)
    args.add_argument('--n_select_sample', type=int, default=1)
    args.add_argument("--concatination", type=str, choices=[True, False],default=True)
    args.add_argument('--split', type=str, choices=['level_5', 'train', 'test'], default='level_5')
    args.add_argument('--category', type=str, choices=['algebra', 'counting_and_probability', 'geometry', 'number_theory', 'precalculus', 'prealgebra', 'intermediate_algebra'], default='algebra')

    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)
