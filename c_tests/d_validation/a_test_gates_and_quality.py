import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.k_validation.a_validation_gate import ValidationGate
from a_platform.l_quality.a_quality_engine import QualityEngine
from a_platform.m_certification.a_certification_engine import CertificationEngine
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.j_runtime.a_execution.c_runtime import ExecutionResult
import os

def test_validation_gate_fails_no_execution():
    vg = ValidationGate()
    ctx = ExecutionContext()
    res = vg.evaluate(ctx, None)
    assert res.passed is False

def test_quality_engine_requires_evidence():
    qe = QualityEngine()
    ctx = ExecutionContext(project_id="test_missing_proj")
    report = qe.evaluate(ctx, validation_result={"passed": False}, runtime_result={"status": "FAILED"})
    assert report.passed is False
    assert report.score < 1.0

def test_certification_fails_on_missing():
    ce = CertificationEngine()
    ctx = ExecutionContext(project_id="test_cert_fail")
    report = ce.evaluate(ctx, execution_result=None, validation_result=None, quality_result=None)
    assert report.passed is False
