python run.py \
    --task math \
    --task_start_index 100 \
    --task_end_index 102 \
    --method_generate sample \
    --method_evaluate value \
    --method_select greedy \
    --n_evaluate_sample 1 \
    --n_select_sample 1 \
    ${@}
