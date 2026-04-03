# STUB: Full implementation in Task 3
def build_arex_conf(app, arex_storage_host: str, arex_storage_port: int) -> str:
    raise NotImplementedError("To be implemented in Task 3")

def get_default_conf_preview() -> str:
    return "# arex.agent.conf\narex.service.name=<your-app-name>\narex.storage.service.host=localhost:8080\narex.enable.debug=false"
