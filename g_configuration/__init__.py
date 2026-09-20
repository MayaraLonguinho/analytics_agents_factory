"""
g_configuration
===============
Pacote de configuração operacional do Analytics Agents Factory (AAF).
Expõe a classe de configuração (AAFSettings / Settings), o singleton global (settings)
e o helper de resolução (get_settings).
"""
from .a_settings import AAFSettings, Settings, get_settings, settings

__all__ = [
    "AAFSettings",
    "Settings",
    "get_settings",
    "settings",
]