from .generic_service import GenericService
from bdaserviceutils import HttpHealthServer

class StreamingService(GenericService):

    def __init__(self, parser):
        super().__init__(parser)
        HttpHealthServer.run_thread()
