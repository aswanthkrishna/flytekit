from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class AWSConfig:
    access_key_id : str
    secret_access_key : str
    default_region_name: Optional[str]
    default_output_format: Optional[str]
    