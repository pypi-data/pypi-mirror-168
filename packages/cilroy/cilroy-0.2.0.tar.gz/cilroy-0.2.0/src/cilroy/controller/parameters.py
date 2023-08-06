from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Optional

from kilroy_server_py_utils import (
    CategorizableBasedParameter,
    OptionalParameter,
    Parameter,
    classproperty,
)

from cilroy.controller.state import State
from cilroy.posting import PostScheduler
from cilroy.scoring import ScoreScheduler


class ScrapBeforeParameter(OptionalParameter[State, str]):
    async def _get(self, state: State) -> Optional[str]:
        if state.offline.scrap_before is None:
            return None
        return state.offline.scrap_before.isoformat()

    async def _set(
        self, state: State, value: Optional[str]
    ) -> Callable[[], Awaitable]:
        original_value = state.offline.scrap_before

        async def undo():
            state.offline.scrap_before = original_value

        state.offline.scrap_before = (
            datetime.fromisoformat(value) if value is not None else None
        )
        return undo

    @classproperty
    def schema(cls) -> Dict[str, Any]:
        return {"type": "string", "format": "date-time"}


class ScrapAfterParameter(OptionalParameter[State, str]):
    async def _get(self, state: State) -> Optional[str]:
        if state.offline.scrap_after is None:
            return None
        return state.offline.scrap_after.isoformat()

    async def _set(
        self, state: State, value: Optional[str]
    ) -> Callable[[], Awaitable]:
        original_value = state.offline.scrap_after

        async def undo():
            state.offline.scrap_after = original_value

        state.offline.scrap_after = (
            datetime.fromisoformat(value) if value is not None else None
        )
        return undo

    @classproperty
    def schema(cls) -> Dict[str, Any]:
        return {"type": "string", "format": "date-time"}


class ScrapLimitParameter(OptionalParameter[State, int]):
    async def _get(self, state: State) -> Optional[int]:
        if state.offline.scrap_limit is None:
            return None
        return state.offline.scrap_limit

    async def _set(
        self, state: State, value: Optional[int]
    ) -> Callable[[], Awaitable]:
        original_value = state.offline.scrap_limit

        async def undo():
            state.offline.scrap_limit = original_value

        state.offline.scrap_limit = value if value is not None else None
        return undo

    @classproperty
    def schema(cls) -> Dict[str, Any]:
        return {"type": "integer", "minimum": 0}


class MaxOfflineEpochsParameter(OptionalParameter[State, int]):
    async def _get(self, state: State) -> Optional[int]:
        if state.offline.max_epochs is None:
            return None
        return state.offline.max_epochs

    async def _set(
        self, state: State, value: Optional[int]
    ) -> Callable[[], Awaitable]:
        original_value = state.offline.max_epochs

        async def undo():
            state.offline.max_epochs = original_value

        state.offline.max_epochs = value if value is not None else None
        return undo

    @classproperty
    def schema(cls) -> Dict[str, Any]:
        return {"type": "integer", "minimum": 0}


class OfflineBatchSizeParameter(OptionalParameter[State, int]):
    async def _get(self, state: State) -> Optional[int]:
        if state.offline.batch_size is None:
            return None
        return state.offline.batch_size

    async def _set(
        self, state: State, value: Optional[int]
    ) -> Callable[[], Awaitable]:
        original_value = state.offline.batch_size

        async def undo():
            state.offline.batch_size = original_value

        state.offline.batch_size = value if value is not None else None
        return undo

    @classproperty
    def schema(cls) -> Dict[str, Any]:
        return {"type": "integer", "minimum": 1}


class PostSchedulerParameter(
    CategorizableBasedParameter[State, PostScheduler]
):
    async def _get_categorizable(self, state: State) -> PostScheduler:
        return state.online.post_scheduler

    async def _set_categorizable(
        self, state: State, value: PostScheduler
    ) -> None:
        state.online.post_scheduler = value

    async def _get_params(self, state: State, category: str) -> Dict[str, Any]:
        return state.online.post_schedulers_params[category]


class ScoreSchedulerParameter(
    CategorizableBasedParameter[State, ScoreScheduler]
):
    async def _get_categorizable(self, state: State) -> ScoreScheduler:
        return state.online.score_scheduler

    async def _set_categorizable(
        self, state: State, value: ScoreScheduler
    ) -> None:
        state.online.score_scheduler = value

    async def _get_params(self, state: State, category: str) -> Dict[str, Any]:
        return state.online.score_schedulers_params[category]


class OnlineIterationsParameter(Parameter[State, int]):
    async def _get(self, state: State) -> int:
        return state.online.iterations

    async def _set(self, state: State, value: int) -> Callable[[], Awaitable]:
        original_value = state.online.iterations

        async def undo():
            state.online.iterations = original_value

        state.online.iterations = value
        return undo

    @classproperty
    def schema(cls) -> Dict[str, Any]:
        return {"type": "integer", "minimum": 0}


class OnlineBatchSizeParameter(OptionalParameter[State, int]):
    async def _get(self, state: State) -> Optional[int]:
        if state.online.batch_size is None:
            return None
        return state.online.batch_size

    async def _set(
        self, state: State, value: Optional[int]
    ) -> Callable[[], Awaitable]:
        original_value = state.online.batch_size

        async def undo():
            state.online.batch_size = original_value

        state.online.batch_size = value if value is not None else None
        return undo

    @classproperty
    def schema(cls) -> Dict[str, Any]:
        return {"type": "integer", "minimum": 1}
