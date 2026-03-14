"""
安全控制器
Security Controller - 安全管理API控制器
"""

from ninja_extra import api_controller, http_delete, http_get, http_post, http_put
from ninja_extra.permissions import AllowAny

from src.api.common.responses import MessageResponse
from src.application.dto.security import (
    IPBlacklistDTO,
    IPBlacklistResponseDTO,
    IPWhitelistDTO,
    IPWhitelistResponseDTO,
    RateLimitRuleDTO,
    RateLimitRuleResponseDTO,
)
from src.application.services.security_service import SecurityService


@api_controller("/v1", tags=["安全"], permissions=[AllowAny])
class SecurityController:
    """
    安全控制器
    处理安全管理相关API请求
    
    遵循SOLID原则:
    - 单一职责: 只处理安全相关的HTTP请求
    - 依赖倒置: 通过构造函数注入 SecurityService
    """
    
    def __init__(self, security_service: SecurityService | None = None) -> None:
        """
        初始化安全控制器
        
        Args:
            security_service: 安全服务实例（可选，用于依赖注入）
        """
        self._security_service = security_service or SecurityService()
    
    # ========== IP黑名单管理 ==========
    
    @http_post(
        "/security/blacklist",
        response=IPBlacklistResponseDTO,
        summary="添加IP到黑名单",
        operation_id="security_add_blacklist"
    )
    async def add_to_blacklist(
        self,
        blacklist_dto: IPBlacklistDTO
    ) -> IPBlacklistResponseDTO:
        """
        添加IP到黑名单
        
        - 禁止指定IP访问
        
        Args:
            blacklist_dto: IP黑名单数据传输对象
            
        Returns:
            IPBlacklistResponseDTO: 创建的黑名单条目
            
        Raises:
            ValueError: 添加失败时抛出
        """
        result = await self._security_service.add_to_blacklist(blacklist_dto)
        return result
    
    @http_delete(
        "/security/blacklist/{ip_address}",
        response=MessageResponse,
        summary="从黑名单移除IP",
        operation_id="security_remove_blacklist"
    )
    async def remove_from_blacklist(self, ip_address: str) -> MessageResponse:
        """
        从黑名单移除IP
        
        - 解除IP的访问禁止
        
        Args:
            ip_address: IP地址
            
        Returns:
            MessageResponse: 操作结果消息
            
        Raises:
            ValueError: IP不在黑名单中时抛出
        """
        result = await self._security_service.remove_from_blacklist(ip_address)
        if not result:
            raise ValueError("IP不在黑名单中")
        return MessageResponse(message="IP已从黑名单移除")
    
    @http_get(
        "/security/blacklist",
        response=list[IPBlacklistResponseDTO],
        summary="获取黑名单列表",
        operation_id="security_list_blacklist"
    )
    async def list_blacklist(self) -> list[IPBlacklistResponseDTO]:
        """
        获取黑名单列表
        
        - 获取所有黑名单IP
        
        Returns:
            list[IPBlacklistResponseDTO]: 黑名单列表
        """
        result = await self._security_service.list_blacklist()
        return result
    
    # ========== IP白名单管理 ==========
    
    @http_post(
        "/security/whitelist",
        response=IPWhitelistResponseDTO,
        summary="添加IP到白名单",
        operation_id="security_add_whitelist"
    )
    async def add_to_whitelist(
        self,
        whitelist_dto: IPWhitelistDTO
    ) -> IPWhitelistResponseDTO:
        """
        添加IP到白名单
        
        - 允许指定IP访问（白名单模式下）
        
        Args:
            whitelist_dto: IP白名单数据传输对象
            
        Returns:
            IPWhitelistResponseDTO: 创建的白名单条目
            
        Raises:
            ValueError: 添加失败时抛出
        """
        result = await self._security_service.add_to_whitelist(whitelist_dto)
        return result
    
    @http_delete(
        "/security/whitelist/{ip_address}",
        response=MessageResponse,
        summary="从白名单移除IP",
        operation_id="security_remove_whitelist"
    )
    async def remove_from_whitelist(self, ip_address: str) -> MessageResponse:
        """
        从白名单移除IP
        
        - 移除IP的访问许可
        
        Args:
            ip_address: IP地址
            
        Returns:
            MessageResponse: 操作结果消息
            
        Raises:
            ValueError: IP不在白名单中时抛出
        """
        result = await self._security_service.remove_from_whitelist(ip_address)
        if not result:
            raise ValueError("IP不在白名单中")
        return MessageResponse(message="IP已从白名单移除")
    
    @http_get(
        "/security/whitelist",
        response=list[IPWhitelistResponseDTO],
        summary="获取白名单列表",
        operation_id="security_list_whitelist"
    )
    async def list_whitelist(self) -> list[IPWhitelistResponseDTO]:
        """
        获取白名单列表
        
        - 获取所有白名单IP
        
        Returns:
            list[IPWhitelistResponseDTO]: 白名单列表
        """
        result = await self._security_service.list_whitelist()
        return result
    
    # ========== 限流规则管理 ==========
    
    @http_post(
        "/security/rate-limit",
        response=RateLimitRuleResponseDTO,
        summary="创建限流规则",
        operation_id="security_create_rate_limit"
    )
    async def create_rate_limit_rule(
        self,
        rule_dto: RateLimitRuleDTO
    ) -> RateLimitRuleResponseDTO:
        """
        创建限流规则
        
        - 为API端点创建访问频率限制
        
        Args:
            rule_dto: 限流规则数据传输对象
            
        Returns:
            RateLimitRuleResponseDTO: 创建的限流规则
            
        Raises:
            ValueError: 创建失败时抛出
        """
        result = await self._security_service.create_rate_limit_rule(rule_dto)
        return result
    
    @http_put(
        "/security/rate-limit/{rule_id}/toggle",
        response=RateLimitRuleResponseDTO,
        summary="切换限流规则状态",
        operation_id="security_toggle_rate_limit"
    )
    async def toggle_rate_limit_rule(self, rule_id: str) -> RateLimitRuleResponseDTO:
        """
        切换限流规则状态
        
        - 启用或禁用限流规则
        
        Args:
            rule_id: 规则ID
            
        Returns:
            RateLimitRuleResponseDTO: 更新后的限流规则
            
        Raises:
            ValueError: 规则不存在时抛出
        """
        result = await self._security_service.toggle_rate_limit_rule(rule_id)
        return result
    
    @http_delete(
        "/security/rate-limit/{rule_id}",
        response=MessageResponse,
        summary="删除限流规则",
        operation_id="security_delete_rate_limit"
    )
    async def delete_rate_limit_rule(self, rule_id: str) -> MessageResponse:
        """
        删除限流规则
        
        - 删除指定的限流规则
        
        Args:
            rule_id: 规则ID
            
        Returns:
            MessageResponse: 操作结果消息
            
        Raises:
            ValueError: 规则不存在时抛出
        """
        result = await self._security_service.delete_rate_limit_rule(rule_id)
        if not result:
            raise ValueError("限流规则不存在")
        return MessageResponse(message="限流规则删除成功")
    
    @http_get(
        "/security/rate-limit",
        response=list[RateLimitRuleResponseDTO],
        summary="获取限流规则列表",
        operation_id="security_list_rate_limits"
    )
    async def list_rate_limit_rules(self) -> list[RateLimitRuleResponseDTO]:
        """
        获取限流规则列表
        
        - 获取所有限流规则
        
        Returns:
            list[RateLimitRuleResponseDTO]: 限流规则列表
        """
        result = await self._security_service.list_rate_limit_rules()
        return result
    
    # ========== 安全状态 ==========
    
    @http_get(
        "/security/status",
        summary="获取安全状态",
        operation_id="security_get_status"
    )
    async def get_security_status(self) -> dict:
        """
        获取安全状态
        
        - 获取当前安全配置状态
        
        Returns:
            dict: 安全状态信息
        """
        result = await self._security_service.get_security_status()
        return result
