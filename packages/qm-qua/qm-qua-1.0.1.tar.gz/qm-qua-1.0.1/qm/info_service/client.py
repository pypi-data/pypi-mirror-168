from grpclib import GRPCError, Status
from grpclib.client import Channel
from qm.io.qualang.api.v1 import InfoServiceStub, GetInfoRequest
from qm.info_service.info import QuaMachineInfo, ImplementationInfo


class ServerInfoException(Exception):
    pass


class QuaClient:
    def __init__(self, *, host: str = "127.0.0.1", port: int = 80, **kwargs) -> None:
        self._host = host
        self._port = port
        self._channel_factory = kwargs.get("grpc_channel_factory", None)
        super().__init__()

    def _create_channel(self):
        if self._channel_factory is not None:
            return self._channel_factory()
        else:
            return Channel(host=self._host, port=self._port)

    async def get_server_info(self):
        async with self._create_channel() as channel:
            service = InfoServiceStub(channel)
            get_info_request = GetInfoRequest()
            try:
                response = await service.get_info(get_info_request)
            except GRPCError as e:
                if e.status == Status.UNKNOWN:
                    raise ServerInfoException("Failed to fetch server info") from e
                else:
                    raise
            return QuaMachineInfo(
                capabilities=response.capabilities,
                implementation=ImplementationInfo(
                    name=response.implementation.name,
                    version=response.implementation.version,
                    url=response.implementation.url,
                ),
            )
