def compute_task_value(task: str) -> float:
    """
    Simple value scoring function for freelance tasks.
    Returns a numeric score based on task length and keywords.
    """

    if not task or not isinstance(task, str):
        return 0.0

    # Base score from length
    length_score = min(len(task) / 10, 10)

    # Keyword multipliers
    keywords = {
        "write": 1.2,
        "design": 1.3,
        "build": 1.4,
        "research": 1.1,
        "analysis": 1.25,
        "proposal": 1.3,
        "client": 1.15,
        "email": 1.05,
        "report": 1.2
    }

    multiplier = 1.0
    for word, factor in keywords.items():
        if word in task.lower():
            multiplier *= factor

    score = length_score * multiplier

    return round(score, 2)
