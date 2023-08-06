import numpy as np
from typing import Optional

class HTML:
    """ A barebones HTML display helper."""
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return self.data

    def _repr_html_(self):
        return self.data

    def __html__(self):
        return self._repr_html_()

    def save(self, filename: str) -> str:
        """Save HTML to file.
        Args:
            filename (str): the filename or path of the file to save.
        Returns:
            The path where the file was saved.
        """
        from os.path import splitext, abspath
        filename, file_ext = splitext(filename)
        if file_ext != '.html':
            from warnings import warn
            warn(f"\n\nBad file extension given '{file_ext}'. Will save as html instead.\n", stacklevel=2)
            file_ext = '.html'

        path = filename + file_ext

        with open(path, "w") as fd:
            fd.write(self._repr_html_())

        return abspath(path)

def get_progress_label(epoch: int, epochs: int, elapsed_seconds: Optional[float] = None, model_count: Optional[int] = None) -> str:
    """Gives a label for use with feyn.show_model based on epochs, max_epochs, time elapsed and model_count

    Arguments:
        epoch {int} -- The current epoch
        epochs {int} -- Total amount of epochs
        elapsed_seconds {Optional[int]} -- seconds elapsed so far
        model_count {Optional[int]} -- Models investigated so far

    Returns:
        str -- A string label displaying progress
    """
    epoch_status = f"Epoch no. {epoch}/{epochs}"
    model_status = ""
    elapsed_status = ""

    if model_count is not None:
        model_status = f" - Tried {model_count} models"
    if elapsed_seconds is not None:
        if epoch < epochs:
            elapsed_status = f" - Elapsed: {_time_to_hms(elapsed_seconds)} of {_time_to_hms(np.ceil(elapsed_seconds/epoch*epochs), most_signif=True)}. (est.)"
        else:
            elapsed_status = f" - Completed in {_time_to_hms(elapsed_seconds)}."

    return f"{epoch_status}{model_status}{elapsed_status}"


def _time_to_hms(tis: float, most_signif: bool = False) -> str:
    s = int(tis % 60)
    m = int(tis // 60 % 60)
    h = int(tis // 3600)
    if most_signif:
        return f"{h + m/60:.1f}h" if h else f"{m+s/60:.1f}m" if m else f"{s}s"
    return f"{h}h {m}m {s}s" if h else f"{m}m {s}s" if m else f"{s}s"
