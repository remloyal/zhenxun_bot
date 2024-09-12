import nonebot

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.utils.image_utils import BuildImage, ImageTemplate

from ._utils import HelpImageBuild

random_bk_path = IMAGE_PATH / "background" / "help" / "simple_help"

background = IMAGE_PATH / "background" / "0.png"


async def create_help_img(bot_id: str, group_id: str | None):
    """生成帮助图片

    参数:
        bot_id: bot id
        group_id: 群号
    """
    await HelpImageBuild().build_image(bot_id, group_id)


async def get_plugin_help(name: str, is_superuser: bool) -> str | BuildImage:
    """获取功能的帮助信息

    参数:
        name: 插件名称或id
        is_superuser: 是否为超级用户
    """
    if name.isdigit():
        plugin = await PluginInfo.get_or_none(id=int(name), load_status=True)
    else:
        plugin = await PluginInfo.get_or_none(name__iexact=name, load_status=True)
    if plugin:
        _plugin = nonebot.get_plugin_by_module_name(plugin.module_path)
        if _plugin and _plugin.metadata:
            items = None
            if is_superuser:
                extra = _plugin.metadata.extra
                if usage := extra.get("superuser_help"):
                    items = {
                        "简介": _plugin.metadata.description,
                        "用法": usage,
                    }
            else:
                items = {
                    "简介": _plugin.metadata.description,
                    "用法": _plugin.metadata.usage,
                }
            if items:
                return await ImageTemplate.hl_page(plugin.name, items)
        return "糟糕! 该功能没有帮助喔..."
    return "没有查找到这个功能噢..."
