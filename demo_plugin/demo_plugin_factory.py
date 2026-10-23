from __future__ import annotations

from typing import TYPE_CHECKING

from one_dragon.base.operation.application.application_factory import (
    ApplicationFactory,
)
from one_dragon.base.operation.application_base import Application

from . import demo_plugin_const
from .demo_plugin import SamplePluginApp

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext


class SamplePluginFactory(ApplicationFactory):
    """示例插件工厂。"""

    def __init__(self, ctx: ZContext):
        ApplicationFactory.__init__(self, demo_plugin_const)
        self.ctx: ZContext = ctx

    def create_application(self, instance_idx: int, group_id: str) -> Application:
        return SamplePluginApp(self.ctx)
