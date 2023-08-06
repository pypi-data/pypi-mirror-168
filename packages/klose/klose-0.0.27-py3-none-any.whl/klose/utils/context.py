import functools
import json
from typing import Any

from pydantic import BaseModel

from klose.config import Config
from klose.excpetions.ParamsException import ParamsError
from klose.request.fatcory import PityResponse
from klose.request.request_pb2 import Response


def error_map(error_type: str, field: str, msg: str = None):
    if "missing" in error_type:
        return f"缺少参数: {field}"
    if "params" in error_type:
        return f"参数: {field} {'不规范' if msg is None else msg}"
    if "not_allowed" in error_type:
        return f"参数: {field} 类型不正确"
    if "type_error" in error_type:
        return f"参数: {field} 类型不合法"


def ctx(role=Config.MEMBER):
    if callable(role):
        @functools.wraps(role)
        async def wrapper(*args, **kwargs):
            try:
                return await role(*args, **kwargs)
            except ParamsError as e:
                return Response(code=101, msg=str(e))
            except Exception as e:
                return Response(code=110, msg=str(e))

        return wrapper

    def permission(func):
        @functools.wraps(func)
        async def wrapper_(*args, **kwargs):
            try:
                if role is not None:
                    user = Context.get_user(args[-1])
                    if user.role < role:
                        return Response(code=403, msg="对不起，你没有权限")
                return await func(*args, **kwargs)
            except ParamsError as e:
                return Response(code=101, msg=str(e))
            except Exception as e:
                return Response(code=110, msg=str(e))

        return wrapper_

    return permission


class UserInfo(BaseModel):
    role: int
    name: str
    email: str
    id: int = None


class Context:

    @staticmethod
    def get_user(context):
        meta = dict(context.invocation_metadata())
        user = json.loads(meta.get("user"))
        return UserInfo(**user)

    @staticmethod
    def parse_args(request, model):
        try:
            data = json.loads(request.requestJson.decode("utf-8"))
            return model(**data)
        except Exception as exc:
            err = error_map(exc.errors()[0]["type"], exc.errors()[0].get("loc", ['unknown'])[-1],
                            exc.errors()[0].get("msg")) if len(exc.errors()) > 0 else "参数解析失败"
            raise ParamsError(err)

    @staticmethod
    def success(data=None, code=0, msg="操作成功"):
        if data is None:
            return Response(code=code, msg=msg, resultJson=b"null")
        return Context.success_json(data, code=code, msg=msg)

    @staticmethod
    def failed(msg, code=110, data=b"null"):
        return Response(code=code, msg=msg, resultJson=data)

    @staticmethod
    def dumps(data: Any, *exclude):
        """
        序列化为bytes
        :param data:
        :param exclude:
        :return:
        """
        return json.dumps(PityResponse.encode_json(data, *exclude), ensure_ascii=False).encode("utf-8")

    @staticmethod
    def success_json(data: Any, *exclude, code=0, msg="操作成功"):
        """
        序列化为bytes并返回response
        :param code:
        :param msg:
        :param data:
        :param exclude:
        :return:
        """
        resp = json.dumps(PityResponse.encode_json(data, *exclude), ensure_ascii=False).encode("utf-8")
        return Response(code=code, msg=msg, resultJson=resp)
