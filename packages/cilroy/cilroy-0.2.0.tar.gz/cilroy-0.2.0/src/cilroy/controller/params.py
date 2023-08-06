from datetime import datetime
from typing import Any, Dict, Optional

from cilroy.models import SerializableModel


class OfflineParams(SerializableModel):
    scrap_before: Optional[datetime] = None
    scrap_after: Optional[datetime] = None
    scrap_limit: Optional[int] = None
    max_epochs: Optional[int] = None
    batch_size: Optional[int] = None


class OnlineParams(SerializableModel):
    post_scheduler_type: str = "interval"
    post_schedulers_params: Dict[str, Dict[str, Any]] = {}
    score_scheduler_type: str = "interval"
    score_schedulers_params: Dict[str, Dict[str, Any]] = {}
    iterations: int = 1
    batch_size: Optional[int] = None


class Params(SerializableModel):
    face_host: str = "localhost"
    face_port: int = 10000
    module_host: str = "localhost"
    module_port: int = 11000
    offline: OfflineParams = OfflineParams()
    online: OnlineParams = OnlineParams()
