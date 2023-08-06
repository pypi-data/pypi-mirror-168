# encoding: utf-8
"""
@project: djangoModel->role_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色API
@created_time: 2022/9/2 15:38
"""
from xj_role.services.role_service import RoleService, RoleTreeService
from ..utils.model_handle import *


class RoleAPIView():
    def tree(self):
        params = parse_data(self)
        res, err = RoleTreeService.role_tree(params.get("role_id", 0))
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=res)

    def list(self):
        params = parse_data(self)
        data, err = RoleService.get_role_list(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
