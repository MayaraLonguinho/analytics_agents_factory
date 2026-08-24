import logging
import os
import json
import re
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.g_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class LearningEngine:
    """
    Guarda logs de erros e correções na Memória (Brain)
    para não repetir os mesmos erros. Sintetiza lições estruturadas via LLM.
    """
    def __init__(self, gateway: LLMGateway = None):
        self.memory_path = os.path.join(os.path.dirname(__file__), "..", "b_brain", "memory.json")
        self.memory = self._load_memory()
        self.gateway = gateway or LLMGateway()

    def _load_memory(self) -> list:
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_memory(self):
        try:
            os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
            with open(self.memory_path, "w") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            logger.error(f"[LearningEngine] Falha ao salvar memória: {e}")

    def log_correction(self, request: ProjectRequest, error_log: str, correction: str):
        logger.info("[LearningEngine] Sintetizando lição no KnowledgeGenerator...")
        
        domain = request.project_plan.domain if request.project_plan else "generic"
        
        prompt = f"""
        Tivemos a seguinte falha:
        {error_log}
        
        A correção aplicada foi:
        {correction}
        
        Sintetize esta correção em um JSON estrito com as chaves:
        "problema", "causa_raiz", "patch_aplicado", "contexto_dominio"
        """
        
        system_prompt = "Você é o KnowledgeGenerator da plataforma AAF. Retorne apenas JSON."
        resp = self.gateway.generate(prompt, system_prompt=system_prompt)
        
        lesson = {
            "problema": "Desconhecido",
            "causa_raiz": "Desconhecida",
            "patch_aplicado": correction,
            "contexto_dominio": domain
        }
        
        if resp.get("success"):
            text = resp.get("text", "")
            match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
            if match:
                text = match.group(1).strip()
            try:
                lesson.update(json.loads(text))
            except json.JSONDecodeError:
                logger.warning("[LearningEngine] Falha ao parsear lição do LLM. Salvando texto bruto.")
                lesson["patch_aplicado"] = text
        
        entry = {
            "project_id": request.project_id,
            "lesson": lesson
        }
        
        logger.info("[LearningEngine] Salvando no BrainUpdater/KnowledgeRegistry...")
        self.memory.append(entry)
        self._save_memory()
        
        # Etapa 7: Estruturar no BrainUpdater
        from a_platform.n_learning.brain_updater import BrainUpdater, KnowledgeItem
        updater = BrainUpdater()
        k_item = KnowledgeItem(
            domain=domain,
            pattern=lesson.get("causa_raiz", "Desconhecida"),
            recommendation=lesson.get("patch_aplicado", correction)
        )
        updater.save_lesson(k_item)
        
        logger.info("[LearningEngine] Correção memorizada com sucesso.")
