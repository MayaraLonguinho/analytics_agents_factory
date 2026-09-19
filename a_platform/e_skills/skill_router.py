"""
SkillRouter — Roteador determinístico de Skills para tarefas e agentes.
Suporta seleção multi-skill (1..N capabilities -> 1..N skills selecionadas),
deduplicação, ordenação topológica por dependências e compatibilidade com seleção unitária.
"""
from dataclasses import dataclass, field
import logging
from typing import Optional, List, Dict, Any, Set
from a_platform.e_skills.skill_index import SkillIndex, SkillMetadata

logger = logging.getLogger(__name__)


class SkillRoutingError(RuntimeError):
    """Exceção levantada quando nenhuma Skill compatível for encontrada ou autorizada."""
    def __init__(
        self,
        message: str,
        capability: Optional[str] = None,
        skill_id: Optional[str] = None,
        agent: Optional[str] = None,
        candidates: Optional[List[str]] = None,
        reason: Optional[str] = None,
        **kwargs: Any
    ):
        super().__init__(message)
        self.capability = capability
        self.skill_id = skill_id
        self.agent = agent
        self.candidates = candidates or []
        self.reason = reason
        self.extra = kwargs


@dataclass
class SkillSelectionItem:
    skill_id: str
    capability: str
    order: int
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "capability": self.capability,
            "order": self.order,
            "dependencies": self.dependencies,
        }


@dataclass
class SkillSelection:
    skills: List[SkillSelectionItem] = field(default_factory=list)

    @property
    def skill_ids(self) -> List[str]:
        return [item.skill_id for item in self.skills]

    def __iter__(self):
        return iter(self.skills)

    def __len__(self):
        return len(self.skills)

    def __getitem__(self, index: int) -> SkillSelectionItem:
        return self.skills[index]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skills": [s.to_dict() for s in self.skills]
        }


class SkillRouter:
    """
    Roteia necessidades (capabilities [1..N], preferred_skills, task context)
    para uma seleção ordenada e deduplicada de Skills (SkillSelection).
    """
    def __init__(
        self,
        index: Optional[SkillIndex] = None,
        skill_index: Optional[SkillIndex] = None,
        domain_registry: Optional[Any] = None
    ):
        self.index = index or skill_index or SkillIndex.get_instance()
        self.domain_registry = domain_registry

    def route_skill(
        self,
        agent_name: str,
        capability: Optional[str] = None,
        preferred_skill: Optional[str] = None,
        skill_id: Optional[str] = None,
        allowed_skills: Optional[List[str]] = None,
        task_description: Optional[str] = None,
        domain_name: Optional[str] = None
    ) -> str:
        """
        Método de seleção unitária com total retrocompatibilidade.
        Internamente utiliza route_selection e retorna o primeiro skill_id selecionado.
        """
        caps = [capability] if capability else []
        prefs = [preferred_skill] if preferred_skill else []
        selection = self.route_selection(
            agent_name=agent_name,
            capabilities=caps,
            preferred_skills=prefs,
            skill_id=skill_id,
            allowed_skills=allowed_skills,
            task_description=task_description,
            domain_name=domain_name
        )
        if not selection.skills:
            raise SkillRoutingError(
                f"Nenhuma Skill encontrada/autorizada para agent={agent_name}, capability={capability}",
                capability=capability,
                agent=agent_name
            )
        return selection.skills[0].skill_id

    def route_many(
        self,
        agent_name: str,
        capabilities: Optional[List[str]] = None,
        preferred_skills: Optional[List[str]] = None,
        allowed_skills: Optional[List[str]] = None,
        task_description: Optional[str] = None,
        domain_name: Optional[str] = None
    ) -> SkillSelection:
        """Alias para route_selection."""
        return self.route_selection(
            agent_name=agent_name,
            capabilities=capabilities,
            preferred_skills=preferred_skills,
            allowed_skills=allowed_skills,
            task_description=task_description,
            domain_name=domain_name
        )

    def route_selection(
        self,
        agent_name: str,
        capabilities: Optional[List[str]] = None,
        preferred_skills: Optional[List[str]] = None,
        capability: Optional[str] = None,
        preferred_skill: Optional[str] = None,
        skill_id: Optional[str] = None,
        allowed_skills: Optional[List[str]] = None,
        task_description: Optional[str] = None,
        domain_name: Optional[str] = None
    ) -> SkillSelection:
        """
        Roteia 1..N capabilities para uma SkillSelection ordenada e deduplicada.
        """
        if allowed_skills is None and domain_name and getattr(self, "domain_registry", None):
            try:
                cfg = self.domain_registry.get_domain_config(domain_name)
                if cfg and "allowed_skills" in cfg:
                    allowed_skills = cfg["allowed_skills"]
            except Exception:
                pass

        # Consolidar inputs de capabilities e preferred_skills
        caps: List[str] = []
        if capabilities:
            caps.extend(capabilities)
        if capability and capability not in caps:
            caps.append(capability)

        prefs: List[str] = []
        if preferred_skills:
            prefs.extend(preferred_skills)
        if preferred_skill and preferred_skill not in prefs:
            prefs.append(preferred_skill)

        # Helpers de autorização
        def _match_allowed(s_id: str) -> bool:
            if allowed_skills is None:
                return True
            s_norm = s_id.replace("_", "-")
            allowed_norm = {a.replace("_", "-") for a in allowed_skills}
            return s_norm in allowed_norm

        def _match_agent(meta: SkillMetadata) -> bool:
            if not agent_name:
                return True
            return agent_name in meta.allowed_agents

        # Caso especial: skill_id explícito direto
        if skill_id and not caps:
            meta = self.index.get(skill_id)
            if meta:
                if not _match_allowed(meta.skill_id):
                    raise SkillRoutingError(
                        f"Skill '{skill_id}' não autorizada pelo domínio. Permitidas: {allowed_skills}",
                        skill_id=skill_id,
                        agent=agent_name,
                        reason="Domínio não autoriza a skill"
                    )
                if not _match_agent(meta):
                    raise SkillRoutingError(
                        f"Skill '{skill_id}' não autorizada para o agente '{agent_name}'. Permitidos: {meta.allowed_agents}",
                        skill_id=skill_id,
                        agent=agent_name,
                        reason="Agente não autorizado para a skill"
                    )
                return SkillSelection(skills=[
                    SkillSelectionItem(skill_id=meta.skill_id, capability=caps[0] if caps else meta.skill_id, order=1, dependencies=[])
                ])
            # Se for um alias legado
            return SkillSelection(skills=[
                SkillSelectionItem(skill_id=skill_id, capability=caps[0] if caps else skill_id, order=1, dependencies=[])
            ])

        # Se não há capabilities, mas há preferred_skills
        if not caps and prefs:
            caps = list(prefs)

        # Se ainda não há capabilities, tentar inferir por task_description
        if not caps and task_description:
            desc_lower = task_description.lower()
            for meta in self.index.find_allowed_for_agent(agent_name):
                if not _match_allowed(meta.skill_id):
                    continue
                for trig in meta.triggers:
                    if trig.lower() in desc_lower and meta.skill_id not in caps:
                        caps.append(meta.skill_id)
                        break

        if not caps:
            raise SkillRoutingError(
                f"Nenhuma capability ou skill especificada para roteamento (agent={agent_name}).",
                agent=agent_name,
                reason="Parâmetros capabilities e task_description vazios"
            )

        # 1. Resolver cada capability
        selected_skills_map: Dict[str, str] = {}  # skill_id -> primary capability
        skill_metadata_map: Dict[str, SkillMetadata] = {}

        for cap in caps:
            chosen_skill: Optional[SkillMetadata] = None

            # 1.1 Checar se há preferred_skill explícita correspondente
            for pref in prefs:
                pref_meta = self.index.get(pref)
                if pref_meta and _match_allowed(pref_meta.skill_id) and _match_agent(pref_meta):
                    # Se a preferred_skill atende a capability ou coincide com ela
                    cap_norm = cap.lower().replace("_", "-")
                    if pref_meta.skill_id.lower().replace("_", "-") == cap_norm or any(c.lower().replace("_", "-") == cap_norm for c in pref_meta.capabilities):
                        chosen_skill = pref_meta
                        break

            # 1.2 Checar exact capability match
            if not chosen_skill:
                exact_matches = self.index.find_by_capability(cap)
                valid_exact = [m for m in exact_matches if _match_allowed(m.skill_id) and _match_agent(m)]
                if valid_exact:
                    chosen_skill = valid_exact[0]

            # 1.3 Checar related capabilities (sem stopwords)
            if not chosen_skill:
                stopwords = {"data", "analysis", "skill", "the", "and", "de", "em"}
                cap_words = set(cap.lower().replace("_", "-").split("-")) - stopwords
                best_score = 0
                for meta in self.index.find_allowed_for_agent(agent_name):
                    if not _match_allowed(meta.skill_id):
                        continue
                    score = 0
                    for c in meta.capabilities:
                        c_words = set(c.lower().replace("_", "-").split("-")) - stopwords
                        common = cap_words.intersection(c_words)
                        if len(common) > score:
                            score = len(common)
                    if score > best_score:
                        best_score = score
                        chosen_skill = meta

            # 1.4 Checar triggers / task description
            if not chosen_skill and task_description:
                desc_lower = task_description.lower()
                for meta in self.index.find_allowed_for_agent(agent_name):
                    if not _match_allowed(meta.skill_id):
                        continue
                    for trig in meta.triggers:
                        if trig.lower() in desc_lower:
                            chosen_skill = meta
                            break
                    if chosen_skill:
                        break

            # Se falhou em resolver esta capability
            if not chosen_skill:
                candidates = [m.skill_id for m in self.index.find_by_capability(cap)]
                reason = "Capability desconhecida no SkillIndex" if not candidates else "Skills candidatas não autorizadas para o agente ou domínio"
                raise SkillRoutingError(
                    f"Falha de roteamento: nenhuma Skill elegível para capability '{cap}' (Agent: '{agent_name}'). Motivo: {reason}. Candidatas: {candidates}",
                    capability=cap,
                    agent=agent_name,
                    candidates=candidates,
                    reason=reason
                )

            # Deduplicação: se a skill já foi selecionada para uma capability anterior, não duplica
            if chosen_skill.skill_id not in selected_skills_map:
                selected_skills_map[chosen_skill.skill_id] = cap
                skill_metadata_map[chosen_skill.skill_id] = chosen_skill
            else:
                logger.debug(f"[SkillRouter] Deduplicação aplicada: skill '{chosen_skill.skill_id}' já selecionada para capability '{selected_skills_map[chosen_skill.skill_id]}', cobrindo também '{cap}'.")

        # 2. Ordenação Topológica com base em depends_on entre as Skills selecionadas
        selected_ids = list(selected_skills_map.keys())
        dependencies_map: Dict[str, List[str]] = {}

        for s_id in selected_ids:
            meta = skill_metadata_map[s_id]
            # Considerar apenas dependências que façam parte da seleção atual
            internal_deps = [dep for dep in getattr(meta, "depends_on", []) if dep in selected_ids]
            dependencies_map[s_id] = internal_deps

        ordered_ids = self._topological_sort(selected_ids, dependencies_map)

        # 3. Montar SkillSelection com order sequencial (1..N)
        items: List[SkillSelectionItem] = []
        for idx, s_id in enumerate(ordered_ids, start=1):
            items.append(
                SkillSelectionItem(
                    skill_id=s_id,
                    capability=selected_skills_map[s_id],
                    order=idx,
                    dependencies=dependencies_map[s_id]
                )
            )

        logger.info(f"[SkillRouter] Seleção multi-skill resolvida para {agent_name}: {[i.skill_id for i in items]}")
        return SkillSelection(skills=items)

    def _topological_sort(self, items: List[str], dependencies: Dict[str, List[str]]) -> List[str]:
        """
        Ordenação topológica estável que preserva a ordem original quando não há restrições.
        """
        in_degree: Dict[str, int] = {item: 0 for item in items}
        dependents: Dict[str, List[str]] = {item: [] for item in items}

        for item in items:
            for dep in dependencies.get(item, []):
                if dep in dependents:
                    dependents[dep].append(item)
                    in_degree[item] += 1

        # Fila inicial com nós que possuem in_degree == 0 mantendo ordem original
        queue = [item for item in items if in_degree[item] == 0]
        sorted_list = []

        while queue:
            curr = queue.pop(0)
            sorted_list.append(curr)
            for neighbor in dependents.get(curr, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Se houver ciclo, faz fallback para a ordem original
        if len(sorted_list) != len(items):
            logger.warning("[SkillRouter] Ciclo detectado nas dependências de skills. Utilizando ordem da task.")
            return items

        return sorted_list
