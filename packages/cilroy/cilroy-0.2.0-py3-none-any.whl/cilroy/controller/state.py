import asyncio
from asyncio import Lock
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, MutableMapping, Optional, Tuple
from uuid import UUID

from kilroy_face_client_py_sdk import FaceService
from kilroy_module_client_py_sdk import ModuleService
from kilroy_server_py_utils import Observable

from cilroy.posting import PostScheduler
from cilroy.scoring import ScoreScheduler
from cilroy.status import TrainingStatus


@dataclass
class OfflineState:
    scrap_before: Optional[datetime]
    scrap_after: Optional[datetime]
    scrap_limit: Optional[int]
    max_epochs: Optional[int]
    batch_size: Optional[int]
    posts_cache: MutableMapping[str, Tuple[Dict, float]]


@dataclass
class OnlineState:
    ids_cache: MutableMapping[UUID, UUID]
    post_scheduler: PostScheduler
    post_schedulers_params: Dict[str, Dict[str, Any]]
    score_scheduler: ScoreScheduler
    score_schedulers_params: Dict[str, Dict[str, Any]]
    iterations: int
    batch_size: Optional[int]
    lock: Lock


@dataclass
class State:
    face_service: FaceService
    module_service: ModuleService
    offline: OfflineState
    online: OnlineState
    training_task: Optional[asyncio.Task]
    training_status: Observable[TrainingStatus]
