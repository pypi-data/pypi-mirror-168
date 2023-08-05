from typing import Optional, List, Tuple

from pydantic import BaseModel, Field

__all__ = ["WPMeta", "WPFAQItem", "WPReadMe", "WPRelease"]


class WPMeta(BaseModel):
    name: str = Field(..., title="")
    contributors: Optional[str] = Field(None)
    donate_link: Optional[str] = Field(None)
    tags: Optional[str] = Field(None)
    requires_at_least: Optional[str] = Field(None)
    tested_up_to: Optional[str] = Field(None)
    stable_tag: Optional[str] = Field(None)
    license: Optional[str] = Field(None)
    license_uri: Optional[str] = Field(None)


class WPFAQItem(BaseModel):
    q: str = Field(..., title="问题")
    a: str = Field(..., title="markdown")


class WPReadMe(BaseModel):
    meta: WPMeta = Field(...)
    intro: Optional[str] = Field(None)
    desc: Optional[str] = Field(None)
    install: Optional[str] = Field(None)
    faq: Optional[List[WPFAQItem]] = Field([], title="FAQ")
    # first is image url, seconds is image alt string
    screenshots: Optional[List[Tuple[str, str]]] = Field([])
    changelog: Optional[str] = Field(None, title="更新日志")
    other_notes: Optional[str] = Field(None, title="其他注释")
    upgrade_notice: Optional[str] = Field(None)
    options: Optional[str] = Field(None)
    further_information: Optional[str] = Field(None)
    template_tag: Optional[str] = Field(None)


class WPRelease(BaseModel):
    name: str = Field(..., title="插件名称", description="slug")
    releases: List[str] = Field([], title="发布版本")
