import pytest
from a_platform.d_skills.d_data_engineering.profiler import DataProfilerSkill, ProfileInput

@pytest.mark.asyncio
async def test_data_profiler_skill():
    profiler = DataProfilerSkill()
    # Path will fail in mocked env, should trigger fallback
    result = await profiler.execute(ProfileInput(filepath="dummy.csv"))
    assert result.rows == 0
    assert result.columns == 0
