from pathlib import Path

from pydantic import BaseModel, Field


class PostProcessing(BaseModel):
    sort_order: str = Field(...)


class SvAnnaToolSpecificConfigurations(BaseModel):
    svanna_jar_executable: Path = Field(...)
    post_process: PostProcessing = Field(...)
