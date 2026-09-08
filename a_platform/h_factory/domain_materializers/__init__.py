"""Registry and dispatch for domain-specific materializers."""

from importlib import import_module
from typing import Dict, Optional, Type

from a_platform.h_factory.artifact_materializer.materializer import ProjectMaterializer

_DOMAIN_MATERIALIZERS: Dict[str, Type[ProjectMaterializer]] = {}


def register_materializer(domain: str, materializer_cls: Type[ProjectMaterializer]) -> None:
    _DOMAIN_MATERIALIZERS[domain.lower()] = materializer_cls


def _load_builtin_materializers() -> None:
    for domain, materializer_name in {
        "analytics": "AnalyticsProjectMaterializer",
        "data_engineering": "DataEngineeringProjectMaterializer",
        "generic": "GenericProjectMaterializer",
    }.items():
        try:
            module = import_module(
                f"g_factory.domain_materializers.{domain}.materializer")
            materializer_cls = getattr(module, materializer_name, None)
            if materializer_cls is not None:
                register_materializer(domain, materializer_cls)
        except ImportError as e:
            import logging
            logging.getLogger(__name__).debug(f"Optional domain materializer not loaded: {e}")


_load_builtin_materializers()


def get_materializer(domain: str) -> Optional[Type[ProjectMaterializer]]:
    key = (domain or "generic").lower()
    materializer = _DOMAIN_MATERIALIZERS.get(key)
    if materializer is not None:
        return materializer

    module_name = {
        "analytics": "g_factory.domain_materializers.analytics.materializer",
        "data_engineering": "g_factory.domain_materializers.data_engineering.materializer",
        "personal_finance": "g_factory.domain_materializers.personal_finance.materializer",
        "crm": "g_factory.domain_materializers.crm.materializer",
        "ecommerce": "g_factory.domain_materializers.ecommerce.materializer",
        "generic": "g_factory.domain_materializers.generic.materializer",
    }.get(key)

    if module_name:
        try:
            import_module(module_name)
        except ImportError as e:
            import logging
            logging.getLogger(__name__).debug(f"Optional domain materializer module not loaded: {e}")
    return _DOMAIN_MATERIALIZERS.get(key)


__all__ = ["register_materializer", "get_materializer"]
