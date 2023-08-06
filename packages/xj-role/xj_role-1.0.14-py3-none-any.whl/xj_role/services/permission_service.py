# encoding: utf-8
"""
@project: djangoModel->user_permission_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户权限服务
@created_time: 2022/8/23 9:33
"""
from django.core.paginator import Paginator
from django.db.models import F

from xj_role.utils.model_handle import format_params_handle
from ..models import RolePermissionValue, UserToRole, Role, RolePermission
from ..utils.j_dict import JDict


# 权限值服务
class PermissionValueService():
    @staticmethod
    def add_permission_value(params):
        """添加权限值"""
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["permission_id", "module", "feature", "permission_value", "type", "relate_key", "relate_value", "config",
                               "is_enable", "is_system", "is_ban", "ban_view", "ban_edit", "ban_add", "ban_delete", "description"]
        )
        if not params:
            return None, "参数不能为空"
        instance = RolePermissionValue.objects.create(**params)
        return {"id": instance.id}, None

    @staticmethod
    def del_permission_value(id):
        # 删除权限值
        if not id:
            return None, "ID 不可以为空"
        instance = RolePermissionValue.objects.filter(id=id)
        if instance:
            instance.delete()
        return None, None

    @staticmethod
    def edit_permission_value(params):
        # 编辑权限值
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "permission_id", "module", "feature", "permission_value", "type", "relate_key", "relate_value", "config",
                               "is_enable", "is_system", "is_ban", "ban_view", "ban_edit", "ban_add", "ban_delete", "description"]
        )
        print(params)
        id = params.pop("id", None)
        if not id:
            return None, "ID 不可以为空"
        if not params:
            return None, "没有可以修改的字段"
        instance = RolePermissionValue.objects.filter(id=id)
        try:
            instance.update(**params)
        except Exception as e:
            return None, "编辑权限错误：" + str(e)
        return None, None

    @staticmethod
    def list(params):
        page = params.pop("page", 1)
        size = params.pop("size", 20)
        params = format_params_handle(param_dict=params, filter_filed_list=["id", "page", "size", "module", "feature", "permission_id"])
        query_set = RolePermissionValue.objects.filter(**params).annotate(permission_name=F("permission__permission_name")).annotate(permission_description=F("permission__description"))
        count = query_set.count()
        query_list = query_set.values() if query_set else []
        finish_set = list(Paginator(query_list, size).page(page).object_list)
        return {"count": count, "page": int(page), "size": int(size), "list": finish_set}, None


# 权限服务
class PermissionService():
    @staticmethod
    def add_permission(params):
        """添加权限值"""
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["permission_id", "permission_name", "description"]
        )
        if not params:
            return None, "参数不能为空"
        RolePermission.objects.create(**params)
        return None, None

    @staticmethod
    def del_permission(permission_id):
        # 删除权限值
        if not permission_id:
            return None, "permission_id 不可以为空"
        instance = RolePermission.objects.filter(permission_id=permission_id)
        if instance:
            instance.delete()
        return None, None

    @staticmethod
    def edit_permission(params):
        # 编辑权限值
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["permission_id", "permission_name", "description"]
        )
        permission_id = params.pop("permission_id", None)
        if not permission_id:
            return None, "ID 不可以为空"
        if not params:
            return None, "没有可以修改的字段"
        instance = RolePermission.objects.filter(permission_id=permission_id)
        try:
            instance.update(**params)
        except Exception as e:
            return None, "编辑权限错误：" + str(e)
        return None, None

    @staticmethod
    def list(params):
        page = params.pop("page", 1)
        size = params.pop("size", 20)
        params = format_params_handle(param_dict=params, filter_filed_list=["permission_id", "permission_name", "description"])
        query_set = RolePermission.objects.filter(**params)
        count = query_set.count()
        query_list = query_set.values() if query_set else []
        finish_set = list(Paginator(query_list, size).page(page).object_list)
        return {"count": count, "page": int(page), "size": int(size), "list": finish_set}, None

    @staticmethod
    def get_group_user(user_id):
        user_role_obj = UserToRole.objects.filter(user_id=user_id).annotate(p_role_id=F("role__parent_role_id"))  # 找到用户的角色ID列表，用于判断同角色，子角色，父角色
        user_roles = user_role_obj.values() if user_role_obj else []
        u_role_ids = [i['role_id'] for i in user_roles]  # 同组
        p_role_ids = [i['p_role_id'] for i in user_roles]  # 父组

        c_role_obj = Role.objects.filter(parent_role_id__in=u_role_ids)
        c_roles = c_role_obj.values() if c_role_obj else []
        c_role_id = [i['id'] for i in c_roles]  # 子组
        res_set = {
            "GROUP_INSIDE": list(set([i['user_id'] for i in list(UserToRole.objects.filter(role_id__in=u_role_ids).values("user_id"))])),
            "GROUP_PARENT": list(set([i['user_id'] for i in list(UserToRole.objects.filter(role_id__in=p_role_ids).values("user_id"))])),
            "GROUP_CHILDREN": list(set([i['user_id'] for i in list(UserToRole.objects.filter(role_id__in=c_role_id).values("user_id"))])),
            "GROUP_OUTSIDE": []
        }
        return res_set, None

    @staticmethod
    def get_user_group_permission(user_id, module=None, feature="ROLE_GROUP", type=None):
        try:
            # 获取用户的权限值 permission_value
            params = {k: v for k, v in {"module": module, "feature": feature}.items() if v}
            permission_set = UserToRole.objects.filter(user_id=user_id).annotate(user_permission_id=F("role__permission_id")).values()
            if not permission_set:
                return {}, None
            permission_dict = [i['user_permission_id'] for i in list(permission_set.values("user_permission_id"))]
            params.setdefault("permission_id__in", list(set(permission_dict)))
            values = list(RolePermissionValue.objects.filter(**params).values(
                "module", "permission_value", "relate_value", "ban_view", "ban_edit", "ban_add", "ban_delete", "is_ban", "is_system", 'is_enable'
            ))
            if not values:
                return {}, None
            res = JDict({})
            group_user, err = PermissionService.get_group_user(user_id)
            for item in values:
                item_copy = JDict(item)
                module_name = item_copy.pop('module')
                res.setdefault(module_name, {})

                current_module = getattr(res, module_name)
                current_module.setdefault('relate_value', item_copy.pop("relate_value"))

                permission_value = item_copy.pop('permission_value')
                item_copy["user_list"] = group_user[permission_value] if permission_value in group_user.keys() else []
                current_module.setdefault(permission_value, item_copy)
            res = res[module] if module else res
            return res, None
        except Exception as e:
            print("msg:" + str(e) + "line:" + str(e.__traceback__.tb_lineno))
            return None, "msg:" + str(e) + "line:" + str(e.__traceback__.tb_lineno)
