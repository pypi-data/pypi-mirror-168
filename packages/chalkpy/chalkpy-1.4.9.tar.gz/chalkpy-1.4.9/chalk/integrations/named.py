import json
import os
from typing import Optional


def has_integration(integration_name: str) -> bool:
    encoded = os.getenv("_CHALK_AVAILABLE_INTEGRATIONS")
    if encoded is not None:
        available = set(json.loads(encoded))
        return integration_name in available
    return False


def load_integration_variable(
    name: str,
    integration_name: Optional[str],
) -> Optional[str]:
    if integration_name is None:
        return os.getenv(name)
    elif has_integration(integration_name):
        return os.getenv(f"{integration_name}_{name}")
    return None
