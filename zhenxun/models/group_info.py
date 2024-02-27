from tortoise import fields

from zhenxun.services.db_context import Model


class GroupInfo(Model):
    group_id = fields.CharField(255, pk=True, description="群组id")
    """群聊id"""
    # channel_id = fields.CharField(255, description="群组id")
    # """频道id"""
    group_name = fields.TextField(default="", description="群组名称")
    """群聊名称"""
    max_member_count = fields.IntField(default=0, description="最大人数")
    """最大人数"""
    member_count = fields.IntField(default=0, description="当前人数")
    """当前人数"""
    group_flag = fields.IntField(default=0, description="群认证标记")
    """群认证标记"""
    block_plugin = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    block_task = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    platform = fields.CharField(255, default="qq", description="所属平台")
    """所属平台"""

    class Meta:
        table = "group_info"
        table_description = "群聊信息表"

    @classmethod
    async def is_block_task(cls, group_id: str, task: str) -> bool:
        """查看群组是否禁用被动

        参数:
            group_id: 群组id
            task: 任务模块

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(group_id=group_id, block_task__contains=f"{task},")

    @classmethod
    def _run_script(cls):
        return [
            "ALTER TABLE group_info ADD group_flag Integer NOT NULL DEFAULT 0;",  # group_info表添加一个group_flag
            "ALTER TABLE group_info ALTER COLUMN group_id TYPE character varying(255);",
            "ALTER TABLE group_info ADD block_plugin Text NOT NULL DEFAULT '';",
            "ALTER TABLE group_info ADD block_task Text NOT NULL DEFAULT '';",
            "ALTER TABLE group_info ADD platform character varying(255) NOT NULL DEFAULT 'qq';",
        ]