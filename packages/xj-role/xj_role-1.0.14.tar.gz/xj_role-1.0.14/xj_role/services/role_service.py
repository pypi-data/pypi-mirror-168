# encoding: utf-8
"""
@project: djangoModel->role_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色服务
@created_time: 2022/9/2 15:37
"""
from django.core.paginator import Paginator

from ..models import Role, UserToRole
from ..utils.model_handle import format_params_handle


# 用户组 树状数据返回
class RoleTreeService(object):
    @staticmethod
    def getTree(data_list, parent_group):
        tree = []
        for item in data_list:
            if str(item['parent_role_id']) == str(parent_group):
                item['name'] = item['role_name']
                item['children'] = RoleTreeService.getTree(data_list, item['id'])
                tree.append(item)
        return tree

    @staticmethod
    def getTrees(data_list, parent_group):
        # 适配模式进行 搜索
        tree = []
        if parent_group != 0:  # 不从根节点搜索，自定义搜索
            base_node = Role.objects.filter(id=parent_group).to_json()  # 如果是搜索，则获取该节点角色信息
            for item in data_list:
                if str(item['parent_role_id']) == str(parent_group):
                    item['name'] = item['role_name']
                    item['children'] = RoleTreeService.getTree(data_list, item['id'])
                    tree.append(item)
            base_node[0]['children'] = tree
            return base_node[0]
        else:  # 进行根节点搜索
            for item in data_list:
                if not str(item['parent_role_id']) == str(parent_group):
                    continue
                child = RoleTreeService.getTree(data_list, item['id'])
                item['name'] = item['role_name']
                item['children'] = child
                tree.append(item)
        return tree

    @staticmethod
    def role_tree(role_id=0):
        data_list = Role.objects.all().to_json()
        group_tree = RoleTreeService.getTrees(data_list, role_id)
        return group_tree, None


class RoleService:
    @staticmethod
    def get_role_list(params, need_pagination=True):
        # 不分页查询
        if not need_pagination:
            params = format_params_handle(
                param_dict=params,
                filter_filed_list=["id", "id_list", "permission_id", "user_group_id", "user_group_id_list"],
                alias_dict={"id_list": "id__in", "user_group_id_list": "user_group_id__in"}
            )
            # print("params:", params)
            query_set = Role.objects.filter(**params)
            if not query_set:
                return [], None
            user_list = list(query_set.values())
            for i in user_list:
                id(i)
                i["is_role"] = True
                i["name"] = i["role_name"]
            return user_list, None
        # 分页查询
        page = params.pop("page", 1)
        size = params.pop("size", 20)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "permission_id", "role", "user_group_id", "page", "size"]
        )
        query_set = Role.objects.filter(**params).values()
        finish_set = list(Paginator(query_set, size).page(page).object_list)
        return finish_set, None

    @staticmethod
    def user_bind_role(user_id, role_id):
        # 用户绑定部门
        if not user_id or not role_id:
            return None, "参数错误，user_id, role_id 必传"
        try:
            UserToRole.objects.get_or_create(
                {"user_id": user_id, "role_id": role_id},
                user_id=user_id,
                role_id=role_id,
            )
            return None, None
        except Exception as e:
            return None, str(e)
