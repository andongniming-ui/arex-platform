# STUB: Full implementation in Task 2
# ArexClient - REST API client for arex-storage service
class ArexClientError(Exception):
    pass

class ArexClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def query_recordings(self, app_id, begin_time, end_time, page_size=50):
        raise NotImplementedError("To be implemented in Task 2")

    async def view_recording(self, record_id):
        raise NotImplementedError("To be implemented in Task 2")

    async def count_recordings(self, app_id, begin_time, end_time):
        raise NotImplementedError("To be implemented in Task 2")

    async def cache_load_mock(self, record_id, target_env=""):
        raise NotImplementedError("To be implemented in Task 2")

    async def cache_remove_mock(self, record_id):
        raise NotImplementedError("To be implemented in Task 2")

    async def health_check(self):
        raise NotImplementedError("To be implemented in Task 2")
