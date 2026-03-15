"""
系统模型
System Models - Django ORM模型定义
包含部门、菜单、菜单元数据、操作日志等模型
"""

import uuid

from django.db import models


class SystemDeptInfo(models.Model):
    """
    部门信息模型
    管理组织架构中的部门信息，支持树形结构
    """

    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex, editable=False)
    mode_type = models.SmallIntegerField(default=0, verbose_name="模式类型")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="描述")
    name = models.CharField(max_length=128, verbose_name="部门名称")
    code = models.CharField(max_length=128, unique=True, db_index=True, verbose_name="部门编码")
    rank = models.IntegerField(default=0, verbose_name="排序")
    auto_bind = models.BooleanField(default=False, verbose_name="自动绑定")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    creator = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_depts", verbose_name="创建者", db_column="creator_id"
    )
    dept_belong = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="belong_depts", verbose_name="归属部门", db_column="dept_belong_id"
    )
    modifier = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="modified_depts", verbose_name="修改者", db_column="modifier_id"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name="上级部门", db_column="parent_id"
    )

    class Meta:
        db_table = "system_deptinfo"
        verbose_name = "部门信息"
        verbose_name_plural = "部门信息"
        ordering = ["rank", "created_time"]
        indexes = [models.Index(fields=["code"]), models.Index(fields=["parent"])]

    def __str__(self) -> str:
        return self.name

    def get_full_path(self) -> str:
        """获取部门完整路径名称"""
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name


class SystemMenuMeta(models.Model):
    """
    菜单元数据模型
    存储菜单的显示配置信息
    """

    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex, editable=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="描述")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="菜单标题")
    icon = models.CharField(max_length=255, blank=True, null=True, verbose_name="图标")
    r_svg_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="SVG图标名称")
    is_show_menu = models.BooleanField(default=True, verbose_name="是否显示菜单")
    is_show_parent = models.BooleanField(default=False, verbose_name="是否显示父级")
    is_keepalive = models.BooleanField(default=True, verbose_name="是否缓存")
    frame_url = models.URLField(blank=True, null=True, verbose_name="iframe地址")
    frame_loading = models.BooleanField(default=False, verbose_name="iframe加载状态")
    transition_enter = models.CharField(max_length=255, blank=True, null=True, verbose_name="进入动画")
    transition_leave = models.CharField(max_length=255, blank=True, null=True, verbose_name="离开动画")
    is_hidden_tag = models.BooleanField(default=False, verbose_name="是否隐藏标签")
    fixed_tag = models.BooleanField(default=False, verbose_name="固定标签")
    dynamic_level = models.IntegerField(default=0, verbose_name="动态层级")
    creator = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_menu_metas", verbose_name="创建者", db_column="creator_id"
    )
    modifier = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="modified_menu_metas", verbose_name="修改者", db_column="modifier_id"
    )

    class Meta:
        db_table = "system_menumeta"
        verbose_name = "菜单元数据"
        verbose_name_plural = "菜单元数据"
        ordering = ["created_time"]

    def __str__(self) -> str:
        return self.title or "未命名菜单"


class SystemMenu(models.Model):
    """
    菜单/权限模型
    权限即菜单，存储系统菜单和权限信息
    """

    MENU_TYPE_CHOICES = [(0, "目录"), (1, "菜单"), (2, "按钮")]

    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex, editable=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="描述")
    menu_type = models.SmallIntegerField(choices=MENU_TYPE_CHOICES, verbose_name="菜单类型")
    name = models.CharField(max_length=128, unique=True, verbose_name="菜单名称")
    rank = models.IntegerField(default=0, verbose_name="排序")
    path = models.CharField(max_length=255, verbose_name="路由路径")
    component = models.CharField(max_length=255, blank=True, null=True, verbose_name="组件路径")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    method = models.CharField(max_length=10, blank=True, null=True, verbose_name="请求方法")
    creator = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_menus", verbose_name="创建者", db_column="creator_id"
    )
    modifier = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="modified_menus", verbose_name="修改者", db_column="modifier_id"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name="父级菜单", db_column="parent_id"
    )
    meta = models.OneToOneField(SystemMenuMeta, on_delete=models.CASCADE, related_name="menu", verbose_name="菜单元数据", db_column="meta_id")

    class Meta:
        db_table = "system_menu"
        verbose_name = "菜单权限"
        verbose_name_plural = "菜单权限"
        ordering = ["rank", "created_time"]
        indexes = [models.Index(fields=["name"]), models.Index(fields=["parent"])]

    def __str__(self) -> str:
        return self.name

    def get_full_path(self) -> str:
        """获取菜单完整路径"""
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name


class SystemOperationLog(models.Model):
    """
    操作记录模型
    记录用户在系统中的所有操作行为
    """

    id = models.BigAutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="描述")
    module = models.CharField(max_length=64, blank=True, null=True, verbose_name="模块名称")
    path = models.CharField(max_length=400, blank=True, null=True, verbose_name="请求路径")
    body = models.TextField(blank=True, null=True, verbose_name="请求体")
    method = models.CharField(max_length=8, blank=True, null=True, verbose_name="请求方法")
    ipaddress = models.CharField(max_length=39, blank=True, null=True, verbose_name="IP地址")
    browser = models.CharField(max_length=64, blank=True, null=True, verbose_name="浏览器")
    system = models.CharField(max_length=64, blank=True, null=True, verbose_name="操作系统")
    response_code = models.IntegerField(blank=True, null=True, verbose_name="响应状态码")
    response_result = models.TextField(blank=True, null=True, verbose_name="响应结果")
    status_code = models.IntegerField(blank=True, null=True, verbose_name="业务状态码")
    creator = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="operation_logs", verbose_name="操作者", db_column="creator_id"
    )
    modifier = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="modified_logs", verbose_name="修改者", db_column="modifier_id"
    )

    class Meta:
        db_table = "system_operationlog"
        verbose_name = "操作记录"
        verbose_name_plural = "操作记录"
        ordering = ["-created_time"]
        indexes = [models.Index(fields=["creator"]), models.Index(fields=["module"]), models.Index(fields=["created_time"])]

    def __str__(self) -> str:
        return f"{self.creator} - {self.module} - {self.method} {self.path}"


class SystemUserRole(models.Model):
    """
    用户角色模型
    角色表，存储角色信息
    """

    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex, editable=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name="描述")
    name = models.CharField(max_length=128, unique=True, verbose_name="角色名称")
    code = models.CharField(max_length=128, unique=True, db_index=True, verbose_name="角色编码")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    creator = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_user_roles", verbose_name="创建者", db_column="creator_id"
    )
    modifier = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="modified_user_roles", verbose_name="修改者", db_column="modifier_id"
    )
    menus = models.ManyToManyField(SystemMenu, through="SystemUserRoleMenu", related_name="roles", verbose_name="菜单权限")

    class Meta:
        db_table = "system_userrole"
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"
        ordering = ["created_time"]
        indexes = [models.Index(fields=["code"]), models.Index(fields=["name"])]

    def __str__(self) -> str:
        return self.name


class SystemUserRoleMenu(models.Model):
    """
    用户角色菜单关联模型
    实现角色与菜单的多对多关系
    """

    id = models.BigAutoField(primary_key=True)
    userrole = models.ForeignKey(SystemUserRole, on_delete=models.CASCADE, related_name="role_menus", verbose_name="角色", db_column="userrole_id")
    menu = models.ForeignKey(SystemMenu, on_delete=models.CASCADE, related_name="role_menus", verbose_name="菜单", db_column="menu_id")

    class Meta:
        db_table = "system_userrole_menu"
        verbose_name = "角色菜单关联"
        verbose_name_plural = "角色菜单关联"
        unique_together = [["userrole", "menu"]]
        indexes = [models.Index(fields=["userrole"]), models.Index(fields=["menu"])]

    def __str__(self) -> str:
        return f"{self.userrole.name} - {self.menu.name}"


class SystemUserInfoRoles(models.Model):
    """
    用户角色关联模型
    实现用户与角色的多对多关系
    """

    id = models.BigAutoField(primary_key=True)
    userinfo = models.ForeignKey("User", on_delete=models.CASCADE, related_name="system_user_roles", verbose_name="用户", db_column="userinfo_id")
    userrole = models.ForeignKey(
        SystemUserRole, on_delete=models.CASCADE, related_name="system_user_roles", verbose_name="角色", db_column="userrole_id"
    )

    class Meta:
        db_table = "system_userinfo_roles"
        verbose_name = "用户角色关联"
        verbose_name_plural = "用户角色关联"
        unique_together = [["userinfo", "userrole"]]
        indexes = [models.Index(fields=["userinfo"]), models.Index(fields=["userrole"])]

    def __str__(self) -> str:
        return f"{self.userinfo.username} - {self.userrole.name}"
