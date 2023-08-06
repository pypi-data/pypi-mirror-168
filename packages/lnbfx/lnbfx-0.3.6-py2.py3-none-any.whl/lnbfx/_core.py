from pathlib import Path
from typing import Optional, Tuple, Union

from lnschema_core import id


class BfxRun:
    def __init__(
        self,
        *,
        pipeline: dict,
        fastq_bcl_path: Union[str, Path, Tuple],
        outdir: Union[str, Path],
        sample_id: Optional[int] = None
    ):
        self._pipeline_id = pipeline["id"]
        self._pipeline_v = pipeline["v"]
        self._pipeline_name = pipeline["name"]
        self._pipeline_reference = pipeline["reference"]
        self._run_id = id.pipeline_run()
        if isinstance(fastq_bcl_path, (str, Path)):
            self._fastq_path = (Path(fastq_bcl_path),)
        else:
            self._fastq_path = (
                Path(fastq_bcl_path[0]),  # type: ignore
                Path(fastq_bcl_path[1]),
            )
        self._outdir = Path(outdir)
        self._sample_id = sample_id
        self._ingested: bool = False
        self._db_engine = None

    @property
    def db_engine(self):
        """Database engine."""
        return self._db_engine

    @property
    def fastq_path(self) -> Tuple:
        """Paths to input fastqs."""
        return self._fastq_path

    @property
    def outdir(self) -> Path:
        """BFX pipeline run dir."""
        return self._outdir

    @property
    def pipeline_id(self):
        """Pipeline id."""
        return self._pipeline_id

    @property
    def pipeline_v(self):
        """Pipeline version."""
        return self._pipeline_v

    @property
    def pipeline_name(self):
        """Pipeline name."""
        return self._pipeline_name

    @property
    def pipeline_reference(self):
        """Pipeline reference."""
        return self._pipeline_reference

    @property
    def run_id(self):
        """Pipeline run id."""
        return self._run_id

    @property
    def run_name(self):
        """Pipeline run name."""
        return self.outdir.as_posix()

    @property
    def sample_id(self):
        """Bfx run's sample id."""
        return self._sample_id
