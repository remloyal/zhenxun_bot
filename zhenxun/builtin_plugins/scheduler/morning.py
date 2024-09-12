import nonebot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_apscheduler import scheduler

from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.configs.config import BotConfig
from zhenxun.models.task_info import TaskInfo
from zhenxun.utils.message import MessageUtils
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.utils.common_utils import CommonUtils
from zhenxun.utils.platform import broadcast_group
from zhenxun.configs.utils import Task, PluginExtraData

__plugin_meta__ = PluginMetadata(
    name="早晚安被动技能",
    description="早晚安被动技能",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
        tasks=[Task(module="morning_goodnight", name="早晚安")],
    ).dict(),
)

driver = nonebot.get_driver()


@driver.on_startup
async def _():
    if not await TaskInfo.exists(module="morning_goodnight"):
        await TaskInfo.create(
            module="morning_goodnight",
            name="早晚安",
            status=True,
        )


async def check(group_id: str) -> bool:
    return not await CommonUtils.task_is_block("morning_goodnight", group_id)


# 早上好
@scheduler.scheduled_job(
    "cron",
    hour=6,
    minute=1,
)
async def _():
    message = MessageUtils.build_message(["早上好", IMAGE_PATH / "zhenxun" / "zao.jpg"])
    await broadcast_group(message, log_cmd="被动早晚安", check_func=check)
    logger.info("每日早安发送...")


# # 睡觉了
@scheduler.scheduled_job(
    "cron",
    hour=23,
    minute=59,
)
async def _():
    message = MessageUtils.build_message(
        [
            f"{BotConfig.self_nickname}要睡觉了，你们也要早点睡呀",
            IMAGE_PATH / "zhenxun" / "sleep.jpg",
        ]
    )
    await broadcast_group(
        message,
        log_cmd="被动早晚安",
        check_func=check,
    )
    logger.info("每日晚安发送...")
