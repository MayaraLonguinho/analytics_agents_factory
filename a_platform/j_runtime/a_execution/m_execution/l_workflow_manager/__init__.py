"""
Workflow Manager Module - Gestão de workflows do Orchestrator Agent
"""

from .a_base_workflow import BaseWorkflowManager
from .c_workflow_manager import WorkflowManager

__all__ = ['BaseWorkflowManager', 'WorkflowManager']
