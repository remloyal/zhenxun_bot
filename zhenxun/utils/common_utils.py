from zhenxun.models.task_info import TaskInfo
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.group_console import GroupConsole


class CommonUtils:

    @classmethod
    async def task_is_block(cls, module: str, group_id: str | None) -> bool:
        """判断被动技能是否可以发送

        参数:
            module: 被动技能模块名
            group_id: 群组id

        返回:
            bool: 是否可以发送
        """
        if task := await TaskInfo.get_or_none(module=module):
            """被动全局状态"""
            if not task.status:
                return True
        if group_id:
            if await GroupConsole.is_block_task(group_id, module):
                """群组是否禁用被动"""
                return True
            if g := await GroupConsole.get_or_none(
                group_id=group_id, channel_id__isnull=True
            ):
                """群组权限是否小于0"""
                if g.level < 0:
                    return True
            if await BanConsole.is_ban(None, group_id):
                """群组是否被ban"""
                return True
        return False
