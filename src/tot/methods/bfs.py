import itertools
import numpy as np
from functools import partial
from src.tot.models import gpt
from src.tot.tree import node, tree

def get_value(task, x, y, n_evaluate_sample, cache_value=True,limit=20):
    value_prompt = task.value_prompt_wrap(x, y)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    #check_gpt_usage(task, limit)
    value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    value = task.value_outputs_unwrap(x, y, value_outputs)
    if cache_value:
        task.value_cache[value_prompt] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True,limit=20):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y.data in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y.data, n_evaluate_sample, cache_value=cache_value,limit=limit)
            local_value_cache[y] = value
        values.append(value)
    return values

def get_votes(task, x, ys, n_evaluate_sample,limit):
    vote_prompt = task.vote_prompt_wrap(x, [y.data for y in ys])
    #check_gpt_usage(task, limit)
    vote_outputs = gpt(vote_prompt, n=n_evaluate_sample, stop=None)
    values = task.vote_outputs_unwrap(vote_outputs, len(ys))
    return values

def get_proposals(task, x, y,limit, step=None):
    propose_prompt = task.propose_prompt_wrap(x, y)
    if not check_gpt_usage(task, limit):
        return
    proposals = gpt(propose_prompt, n=1, stop=None)[0].split('\n')
    proposals_list = []
    for p in proposals:
        if p and p != y:
            if 'step alternative #' in p:
                p = f'Step {step}:' + p.split(':', 1)[1]
            proposals_list.append(y + p + '\n')
    return proposals_list

def get_samples(task, x, y, n_generate_sample, prompt_sample, stop,limit,concotation=True):
    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x, y)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x, y)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    check_gpt_usage(task, limit,n=n_generate_sample)
    samples = gpt(prompt, n=n_generate_sample, stop=stop)
    if concotation:
        return [y + _ for _ in samples]
    else:
        return samples

def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    infos = []
    lim = args.limit
    select_new_ys = ['']
    tracker = tree(task.steps)
    tracker.index = idx
    start_node = node('')
    start_node.index = tracker.get_id()
    tracker.parent = start_node
    ys = [start_node]  # current output candidates
    for step in range(task.steps):
        # generation
        if args.method_generate == 'sample':
            new_ys = []
            for y in ys:
                samples = get_samples(task, x, y.data, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step],limit=lim,concotation=args.concatination)
                for sample in samples:
                    current_node = node(sample)
                    current_node.index = tracker.get_id()
                    current_node.parent = y.index
                    tracker.add_node(current_node,step)
                    new_ys.append(current_node)
        elif args.method_generate == 'propose':
            new_ys = []
            for y in ys:
                proposals = get_proposals(task, x, y.data,limit=lim,step=step+1)
                for proposal in proposals:
                    if not proposal:
                        continue
                    current_node = node(proposal)
                    current_node.index = tracker.get_id()
                    current_node.parent = y.index
                    tracker.add_node(current_node,step)
                    new_ys.append(current_node)
        ids = list(range(len(new_ys)))
        # evaluation
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample, limit=lim)
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample, limit=lim)

        # selection
        if args.method_select == 'sample':
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        elif args.method_select == 'greedy':
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        select_new_ys = [new_ys[select_id] for select_id in select_ids]

        # log
        if to_print: 
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {[y.data for y in sorted_new_ys]}\n-- sol values --: {sorted_values}\n-- choices --: {[y.data for y in select_new_ys]}\n')
        
        infos.append({'step': step, 'x': x, 'ys': [y.data for y in ys], 'new_ys': [y.data for y in new_ys], 'values': values, 'select_new_ys': [y.data for y in select_new_ys]})

        ys = select_new_ys
        for s in select_new_ys:
            if 'final answer: ' in s.data.lower():
                task.stop_iteration = True

        if (hasattr(task, "gpt_limit_reached") and task.gpt_limit_reached):
            final_result = gpt_overuse(task,x,select_new_ys[0].data)
            infos.append({'step': step, 'x': x, "final_result":final_result})
            current_node = node(final_result)
            current_node.index = tracker.get_id()
            current_node.parent = select_new_ys[0].index
            tracker.add_node(current_node,step+1)
            ys = [select_new_ys[0].data + "\n" + final_result]
            task.gpt_usage = 0
            task.gpt_limit_reached = False
            break

        if task.stop_iteration:
            break
    ys = [y.data if isinstance(y, node) else y for y in ys]
    if to_print: 
        print(ys)
    return ys, {'steps': infos},tracker

def naive_solve(args, task, idx, to_print=True):
    global gpt
    check_gpt_usage(task, args.limit)
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None)
    return ys, {}

def check_gpt_usage(task, limit,n=1):
    if not hasattr(task, "gpt_usage") or not hasattr(task, "gpt_limit_reached"):
        return True
    task.gpt_usage += n
    print(f'gpt usage {task.gpt_usage}')
    if task.gpt_usage >= limit:
        task.gpt_limit_reached = True
        return False
    return True


def gpt_overuse(task, x, y):
    prompt = task.gpt_overuse_wrap(x, y)
    final = gpt(prompt=prompt, n=1, stop=None)[0].split('\n')[-1]
    return final
