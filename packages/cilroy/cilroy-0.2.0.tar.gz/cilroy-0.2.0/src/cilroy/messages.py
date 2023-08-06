from dataclasses import dataclass
from typing import List

import betterproto


class Status(betterproto.Enum):
    STATUS_UNSPECIFIED = 0
    STATUS_LOADING = 1
    STATUS_READY = 2


class TrainingStatus(betterproto.Enum):
    TRAINING_STATUS_UNSPECIFIED = 0
    TRAINING_STATUS_IDLE = 1
    TRAINING_STATUS_OFFLINE = 2
    TRAINING_STATUS_ONLINE = 3


@dataclass(eq=False, repr=False)
class GetFaceMetadataRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetFaceMetadataResponse(betterproto.Message):
    key: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class GetModuleMetadataRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetModuleMetadataResponse(betterproto.Message):
    key: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class GetFacePostSchemaRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetFacePostSchemaResponse(betterproto.Message):
    schema: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GetModulePostSchemaRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetModulePostSchemaResponse(betterproto.Message):
    schema: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GetControllerStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetControllerStatusResponse(betterproto.Message):
    status: "Status" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class WatchControllerStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchControllerStatusResponse(betterproto.Message):
    status: "Status" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class GetFaceStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetFaceStatusResponse(betterproto.Message):
    status: "Status" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class WatchFaceStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchFaceStatusResponse(betterproto.Message):
    status: "Status" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class GetModuleStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetModuleStatusResponse(betterproto.Message):
    status: "Status" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class WatchModuleStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchModuleStatusResponse(betterproto.Message):
    status: "Status" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class GetTrainingStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetTrainingStatusResponse(betterproto.Message):
    status: "TrainingStatus" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class WatchTrainingStatusRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchTrainingStatusResponse(betterproto.Message):
    status: "TrainingStatus" = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class GetControllerConfigSchemaRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetControllerConfigSchemaResponse(betterproto.Message):
    schema: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GetControllerConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetControllerConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class WatchControllerConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchControllerConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class SetControllerConfigRequest(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class SetControllerConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GetFaceConfigSchemaRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetFaceConfigSchemaResponse(betterproto.Message):
    schema: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GetFaceConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetFaceConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class WatchFaceConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchFaceConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class SetFaceConfigRequest(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class SetFaceConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GetModuleConfigSchemaRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetModuleConfigSchemaResponse(betterproto.Message):
    schema: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class GetModuleConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetModuleConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class WatchModuleConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchModuleConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class SetModuleConfigRequest(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class SetModuleConfigResponse(betterproto.Message):
    config: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class TrainOfflineRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class TrainOfflineResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class TrainOnlineRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class TrainOnlineResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class StopTrainingRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class StopTrainingResponse(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class MetricConfig(betterproto.Message):
    id: str = betterproto.string_field(1)
    label: str = betterproto.string_field(2)
    config: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class GetModuleMetricsConfigRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class GetModuleMetricsConfigResponse(betterproto.Message):
    configs: List["MetricConfig"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class WatchModuleMetricsRequest(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class WatchModuleMetricsResponse(betterproto.Message):
    metric_id: str = betterproto.string_field(1)
    dataset_id: int = betterproto.uint64_field(2)
    data: str = betterproto.string_field(3)
