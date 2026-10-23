from __future__ import annotations

from typing import TYPE_CHECKING

from one_dragon.base.operation.application_base import Application

from . import demo_plugin_const
from .utils.helper import build_status_message

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext


class SamplePluginApp(Application):
    """示例插件应用。"""

    def __init__(self, ctx: ZContext):
        Application.__init__(
            self,
            ctx,
            demo_plugin_const.APP_ID,
            node_max_retry_times=3,
        )

    def _execute_one_round(self):
        return self.round_success(build_status_message())
