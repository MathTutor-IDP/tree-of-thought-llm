python run.py \
    --task math \
    --task_start_index 1000 \
    --task_end_index 1010 \
    --method_generate propose \
    --method_evaluate value \
    --method_select greedy \
    --n_evaluate_sample 3 \
    --n_select_sample 1 \
    --backend gpt-3.5-turbo \
    ${@}
