def infer_available_threads() -> int:
    """ Attempt to infer the amount of threads available. Will always leave one free for system use.

    Returns:
        int -- thread count
    """
    from os import cpu_count
    found_cpus = cpu_count()
    if found_cpus is None:
        threads = 4
    else:
        threads = found_cpus - 1
    return threads

def kind_to_output_stype(kind: str) -> str:
    """Parse kind into an output spec for the QLattice."""
    if kind in ["regression", "regressor"]:
        return "f"
    if kind in ["classification", "classifier"]:
        return "b"
    raise ValueError("Model kind not understood. Please choose either a 'regression' or a 'classification'.")
