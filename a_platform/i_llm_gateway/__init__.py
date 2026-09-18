"""Canonical LLM Gateway for Analytics AI Factory.

This module provides the single allowed path for agent/skill access to LLM providers.
Agents and Skills must not import provider SDKs directly; they must route through this gateway.
"""

from .d_gateway import LLMGateway, LLMGatewayConfig
from .a_interfaces.a_base_provider import LLMRequest, LLMResponse

__all__ = ["LLMGateway", "LLMGatewayConfig", "LLMRequest", "LLMResponse"]
