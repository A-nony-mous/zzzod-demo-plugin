from one_dragon_qt.services.app_setting.app_setting_provider import (
    AppSettingProvider,
    SettingType,
)

from .demo_plugin_const import APP_ID


class SamplePluginAppSetting(AppSettingProvider):
    """示例插件设置入口。"""

    app_id = APP_ID
    setting_type = SettingType.INTERFACE

    @staticmethod
    def get_setting_cls() -> type:
        from .demo_plugin_setting_interface import SamplePluginSettingInterface

        return SamplePluginSettingInterface
