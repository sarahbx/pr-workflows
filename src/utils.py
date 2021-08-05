def get_labels(pull):
    return [label.name for label in pull.get_labels()]
