def get_task(name, split=None, category=None):
    if name == 'game24':
        from tot.tasks.game24 import Game24Task
        return Game24Task()
    elif name == 'text':
        from tot.tasks.text import TextTask
        return TextTask()
    elif name == 'crosswords':
        from tot.tasks.crosswords import MiniCrosswordsTask
        return MiniCrosswordsTask()
    elif name == 'math':
        from tot.tasks.math_reasoning import MathTask
        if split is not None and category is not None:
            return MathTask('src/tot/data/math/', split, category)
        return MathTask('src/tot/data/math/')
    else:
        raise NotImplementedError
