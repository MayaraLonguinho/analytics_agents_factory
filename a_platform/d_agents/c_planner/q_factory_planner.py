"""Project Planner - Converts discovery results into executable project plans."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from a_core.b_domain.project import DiscoveryResult
# pyrefly: ignore [missing-import]
from a_platform.c_brain.registry import BrainRegistry
from a_platform.i_domains.registry import DomainRegistry, get_domain_registry
from a_core.b_domain.architecture import ArchitectureDecision
from .bundle import ProjectGenerationBundle, ProjectTask


class ProjectPlanner:
    """Bridges Discovery → Brain → Planning → Factory.

    Takes a DiscoveryResult and Brain knowledge, produces a ProjectGenerationBundle.
    """

    def __init__(
        self,
        domain_registry: Optional[DomainRegistry] = None,
        knowledge_registry: Optional[BrainRegistry] = None,
    ):
        self.domain_registry = domain_registry or get_domain_registry()
        self.knowledge_registry = knowledge_registry

    def plan(self, discovery: DiscoveryResult, architecture: Optional[ArchitectureDecision] = None) -> ProjectGenerationBundle:
        """Convert discovery result into a project generation bundle."""
        domain = discovery.domain or "analytics"
        domain_template = self.domain_registry.get_domain(domain)

        if not domain_template:
            raise ValueError(f"Domain not found: {domain}")

        project_name = discovery.project_objective or discovery.request or "Untitled Project"
        # Create bundle
        bundle = ProjectGenerationBundle(
            project_id=self._generate_project_id(project_name),
            project_name=project_name,
            project_description=discovery.request or "",
            domain=domain,
            stack=domain_template.stack,
            created_at=datetime.utcnow().isoformat(),
            created_by="planner",
        )

        # Plan architecture based on domain and requirements
        bundle.architecture = self._plan_architecture(
            domain_template, discovery, architecture)

        # Create task execution plan
        bundle.phases = [phase.name for phase in domain_template.phases]
        bundle.tasks = self._create_tasks(domain_template, discovery)

        # Assign agents and skills
        bundle.agents = self._assign_agents(domain_template, bundle.tasks)
        bundle.skills = domain_template.required_skills
        bundle.mcps = domain_template.required_mcps

        # Define artifacts and outputs
        bundle.artifacts = self._plan_artifacts(domain_template)
        bundle.output_directories = self._plan_directories(domain_template)

        # Runtime configuration
        bundle.runtime_config = self._plan_runtime(domain_template, discovery)

        # Quality and validation requirements
        bundle.quality_requirements = self._plan_quality(domain_template)
        bundle.validation_requirements = self._plan_validation(domain_template)
        bundle.certification_requirements = self._plan_certification(
            domain_template)

        # Estimate cost and dependencies
        bundle.dependencies = self._resolve_dependencies(bundle.tasks)
        bundle.estimated_cost = self._estimate_cost(bundle.tasks)
        bundle.cost_breakdown = self._break_down_cost(bundle.tasks)

        # Add metadata from discovery
        bundle.metadata = {
            "discovery_confidence": discovery.confidence if hasattr(discovery, "confidence") else 0.8,
            "dataset_source": discovery.dataset_source or "",
            "dataset_profile": discovery.dataset_profile if hasattr(discovery, "dataset_profile") else {},
            "requirements": discovery.requirements if hasattr(discovery, "requirements") else {},
            "technology_preferences": discovery.technology_preferences if hasattr(discovery, "technology_preferences") else [],
            "architecture_constraints": discovery.architecture_constraints if hasattr(discovery, "architecture_constraints") else [],
        }

        return bundle

    def _generate_project_id(self, project_name: str, version: str = "1") -> str:
        """Generate a unique project ID."""
        import re
        from datetime import datetime
        now = datetime.now()
        clean_name = re.sub(r'[^a-z0-9]+', '_', project_name.lower()).strip('_')
        if not clean_name:
            clean_name = "project"
        date_str = now.strftime("%y%m%d_%H%M")
        return f"{clean_name}_v{version}_{date_str}"

    def _plan_architecture(self, domain_template: Any, discovery: DiscoveryResult, architecture: Optional[ArchitectureDecision] = None) -> Dict[str, Any]:
        """Plan the architecture based on domain and discovery."""
        backend = architecture.backend if architecture else domain_template.stack.get("backend", "FastAPI")
        frontend = architecture.frontend if architecture else domain_template.stack.get("frontend_framework", "React")
        database = architecture.database if architecture else domain_template.stack.get("database", "PostgreSQL")
        container = architecture.infrastructure if architecture else domain_template.stack.get("container", "Docker")
        
        return {
            "domain": domain_template.domain,
            "pattern": domain_template.materializer_strategy,
            "layers": {
                "backend": backend,
                "frontend": frontend,
                "database": database,
                "container": container,
            },
            "infrastructure": {
                "containerization": True,
                "orchestration": "Docker Compose",
                "deployment": "local",
            },
            "constraints": discovery.architecture_constraints if hasattr(discovery, "architecture_constraints") else [],
            "technology_preferences": discovery.technology_preferences if hasattr(discovery, "technology_preferences") else [],
        }

    def _create_tasks(self, domain_template: Any, discovery: DiscoveryResult) -> List[Dict[str, Any]]:
        """Create task specifications from domain phases."""
        tasks = []
        for phase_idx, phase in enumerate(domain_template.phases):
            task = ProjectTask(
                task_id=f"task_{phase_idx + 1:02d}_{phase.name}",
                name=f"Phase: {phase.name}",
                description=phase.description,
                phase=phase.name,
                agent_roles=phase.agent_roles,
                required_skills=phase.skills_required,
                required_mcps=[],
                dependencies=phase.dependencies,
                outputs=phase.outputs,
                estimated_hours=phase.duration_estimate_hours,
                priority=1 if phase_idx < 3 else 2,
                parallelizable=len(phase.dependencies) == 0 or phase.name in [
                    "backend", "frontend"],
            )
            tasks.append(task.model_dump())
        return tasks

    def _assign_agents(self, domain_template: Any, tasks: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Assign tasks to agents."""
        assignments: Dict[str, List[str]] = {}
        for task in tasks:
            for role in task.get("agent_roles", []):
                if role not in assignments:
                    assignments[role] = []
                assignments[role].append(task["task_id"])
        return assignments

    def _plan_artifacts(self, domain_template: Any) -> List[Dict[str, Any]]:
        """Plan output artifacts."""
        artifacts = []
        for phase in domain_template.phases:
            for output in phase.outputs:
                artifacts.append({
                    "name": output,
                    "type": "code" if output.endswith(".py") else "config",
                    "phase": phase.name,
                    "description": f"Output from {phase.name} phase",
                })
        return artifacts

    def _plan_directories(self, domain_template: Any) -> Dict[str, str]:
        """Plan output directory structure."""
        return {
            "root": ".",
            "backend": "src/backend" if "backend" in domain_template.stack else "",
            "frontend": "src/frontend" if "frontend" in domain_template.stack else "",
            "database": "database" if "database" in domain_template.stack else "",
            "tests": "tests",
            "docs": "docs",
            "infrastructure": "infrastructure",
        }

    def _plan_runtime(self, domain_template: Any, discovery: DiscoveryResult) -> Dict[str, Any]:
        """Plan runtime configuration."""
        return {
            "database": {
                "type": domain_template.stack.get("database", "PostgreSQL"),
                "host": "localhost",
                "port": 5432,
                "name": "project_db",
            },
            "container": {
                "enabled": True,
                "runtime": "docker",
                "orchestration": "compose",
            },
            "environment": "development",
            "requirements": discovery.requirements if hasattr(discovery, "requirements") else {},
        }

    def _plan_quality(self, domain_template: Any) -> Dict[str, Any]:
        """Plan quality requirements."""
        return {
            "code_coverage": 80,
            "linting": True,
            "type_checking": True,
            "security_scan": True,
            "performance_baseline": "established",
        }

    def _plan_validation(self, domain_template: Any) -> List[str]:
        """Plan validation gates."""
        return [
            "structure_validation",
            "dependency_validation",
            "security_validation",
            "performance_validation",
            "documentation_validation",
        ]

    def _plan_certification(self, domain_template: Any) -> Dict[str, Any]:
        """Plan certification requirements."""
        return {
            "required": True,
            "validators": ["structure", "completeness", "quality", "security"],
            "pass_threshold": 0.95,
        }

    def _resolve_dependencies(self, tasks: List[Dict[str, Any]]) -> List[tuple[str, str]]:
        """Resolve task dependencies."""
        dependencies = []
        for task in tasks:
            for dep in task.get("dependencies", []):
                # Find the task that provides this dependency
                for other_task in tasks:
                    if other_task.get("phase") == dep:
                        dependencies.append(
                            (task["task_id"], other_task["task_id"]))
                        break
        return dependencies

    def _estimate_cost(self, tasks: List[Dict[str, Any]]) -> float:
        """Estimate project cost based on tasks."""
        total_hours = sum(task.get("estimated_hours", 0) for task in tasks)
        hourly_rate = 150  # USD
        return total_hours * hourly_rate

    def _break_down_cost(self, tasks: List[Dict[str, Any]]) -> Dict[str, float]:
        """Break down cost by phase."""
        breakdown: Dict[str, float] = {}
        hourly_rate = 150  # USD
        for task in tasks:
            phase = task.get("phase", "unknown")
            hours = task.get("estimated_hours", 0)
            breakdown[phase] = breakdown.get(phase, 0) + (hours * hourly_rate)
        return breakdown
