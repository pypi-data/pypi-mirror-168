from collections import namedtuple

from lnschema_core import id

PIPELINES = {
    "cell_ranger_v7_0_0": {
        "id": id.pipeline(),
        "v": "7.0.0",
        "name": "Cell Ranger v7.0.0",
        "reference": (
            "https://support.10xgenomics.com/"
            "single-cell-gene-expression/software/downloads/latest"
        ),
    },
    "cell_ranger_v7_0_1": {
        "id": id.pipeline(),
        "v": "7.0.1",
        "name": "Cell Ranger v7.0.1",
        "reference": (
            "https://support.10xgenomics.com/"
            "single-cell-gene-expression/software/downloads/latest"
        ),
    },
}


def _lookup(values: dict):
    """Look up a list of values via tab completion."""
    nt = namedtuple("Pipeline", list(values.keys()))  # type: ignore
    return nt(**{key: value for key, value in values.items()})


class lookup:
    pipeline = _lookup(values=PIPELINES)
