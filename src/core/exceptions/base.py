"""
基础API异常
Base API Exception - 所有自定义异常的基类
"""


class BaseAPIError(Exception):
    """
    基础API异常
    所有自定义异常的基类

    属性:
        message: 错误消息
        code: 错误代码
    """

    def __init__(self, message: str = "服务器错误", code: str = "SERVER_ERROR"):
        """
        初始化基础异常

        参数:
            message: 错误消息
            code: 错误代码
        """
        self.message = message
        self.code = code
        super().__init__(self.message)

    def to_dict(self) -> dict[str, str]:
        """
        转换为字典格式

        返回:
            包含消息和代码的字典
        """
        return {"message": self.message, "code": self.code}
