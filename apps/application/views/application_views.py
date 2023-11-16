# coding=utf-8
"""
    @project: maxkb
    @Author：虎
    @file： application_views.py
    @date：2023/10/27 14:56
    @desc:
"""

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.views import APIView

from application.serializers.application_serializers import ApplicationSerializer
from application.swagger_api.application_api import ApplicationApi
from common.auth import TokenAuth, has_permissions
from common.constants.permission_constants import CompareConstants, PermissionConstants, Permission, Group, Operate, \
    ViewPermission, RoleConstants
from common.exception.app_exception import AppAuthenticationFailed
from common.response import result
from common.util.common import query_params_to_single_dict
from dataset.serializers.dataset_serializers import DataSetSerializers


class Application(APIView):
    authentication_classes = [TokenAuth]

    class Profile(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary="获取应用相关信息",
                             operation_id="获取应用相关信息",
                             tags=["应用/会话"])
        def get(self, request: Request):
            if 'application_id' in request.auth.keywords:
                return result.success(ApplicationSerializer.Operate(
                    data={'application_id': request.auth.keywords.get('application_id'),
                          'user_id': request.user.id}).profile())
            else:
                raise AppAuthenticationFailed(401, "身份异常")

    class ApplicationKey(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['POST'], detail=False)
        @swagger_auto_schema(operation_summary="新增ApiKey",
                             operation_id="新增ApiKey",
                             tags=['应用/API_KEY'],
                             manual_parameters=ApplicationApi.ApiKey.get_request_params_api())
        @has_permissions(ViewPermission(
            [RoleConstants.ADMIN, RoleConstants.USER],
            [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.MANAGE,
                                            dynamic_tag=keywords.get('application_id'))],
            compare=CompareConstants.AND))
        def post(self, request: Request, application_id: str):
            return result.success(
                ApplicationSerializer.ApplicationKeySerializer(
                    data={'application_id': application_id, 'user_id': request.user.id}).generate())

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary="获取应用API_KEY列表",
                             operation_id="获取应用API_KEY列表",
                             tags=['应用/API_KEY'],
                             manual_parameters=ApplicationApi.ApiKey.get_request_params_api()
                             )
        @has_permissions(ViewPermission(
            [RoleConstants.ADMIN, RoleConstants.USER],
            [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.MANAGE,
                                            dynamic_tag=keywords.get('application_id'))],
            compare=CompareConstants.AND))
        def get(self, request: Request, application_id: str):
            return result.success(ApplicationSerializer.ApplicationKeySerializer(
                data={'application_id': application_id, 'user_id': request.user.id}).list())

        class Operate(APIView):
            authentication_classes = [TokenAuth]

            @action(methods=['DELETE'], detail=False)
            @swagger_auto_schema(operation_summary="删除应用API_KEY",
                                 operation_id="删除应用API_KEY",
                                 tags=['应用/API_KEY'],
                                 manual_parameters=ApplicationApi.ApiKey.Operate.get_request_params_api())
            @has_permissions(ViewPermission(
                [RoleConstants.ADMIN, RoleConstants.USER],
                [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.MANAGE,
                                                dynamic_tag=keywords.get('application_id'))],
                compare=CompareConstants.AND), lambda r, k: Permission(group=Group.APPLICATION, operate=Operate.DELETE,
                                                                       dynamic_tag=k.get('application_id')),
                compare=CompareConstants.AND)
            def delete(self, request: Request, application_id: str, api_key_id: str):
                return result.success(
                    ApplicationSerializer.ApplicationKeySerializer.Operate(
                        data={'application_id': application_id, 'user_id': request.user.id,
                              'api_key_id': api_key_id}).delete())

    class AccessToken(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['PUT'], detail=False)
        @swagger_auto_schema(operation_summary="修改 应用AccessToken",
                             operation_id="修改 应用AccessToken",
                             tags=['应用/公开访问'],
                             manual_parameters=ApplicationApi.AccessToken.get_request_params_api(),
                             request_body=ApplicationApi.AccessToken.get_request_body_api())
        @has_permissions(ViewPermission(
            [RoleConstants.ADMIN, RoleConstants.USER],
            [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.MANAGE,
                                            dynamic_tag=keywords.get('application_id'))],
            compare=CompareConstants.AND))
        def put(self, request: Request, application_id: str):
            return result.success(
                ApplicationSerializer.AccessTokenSerializer(data={'application_id': application_id}).edit(request.data))

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary="获取应用 AccessToken信息",
                             operation_id="获取应用 AccessToken信息",
                             manual_parameters=ApplicationApi.AccessToken.get_request_params_api(),
                             tags=['应用/公开访问'],
                             )
        @has_permissions(ViewPermission(
            [RoleConstants.ADMIN, RoleConstants.USER],
            [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.USE,
                                            dynamic_tag=keywords.get('application_id'))],
            compare=CompareConstants.AND))
        def get(self, request: Request, application_id: str):
            return result.success(
                ApplicationSerializer.AccessTokenSerializer(data={'application_id': application_id}).one())

    class Authentication(APIView):
        @action(methods=['POST'], detail=False)
        @swagger_auto_schema(operation_summary="应用认证",
                             operation_id="应用认证",
                             request_body=ApplicationApi.Authentication.get_request_body_api(),
                             tags=["应用/认证"],
                             security=[])
        def post(self, request: Request):
            return result.success(
                ApplicationSerializer.Authentication(data={'access_token': request.data.get("access_token")}).auth())

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(operation_summary="创建应用",
                         operation_id="创建应用",
                         request_body=ApplicationApi.Create.get_request_body_api(),
                         tags=['应用'])
    @has_permissions(PermissionConstants.APPLICATION_CREATE, compare=CompareConstants.AND)
    def post(self, request: Request):
        ApplicationSerializer.Create(data={'user_id': request.user.id}).insert(request.data)
        return result.success(True)

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(operation_summary="获取应用列表",
                         operation_id="获取应用列表",
                         manual_parameters=ApplicationApi.Query.get_request_params_api(),
                         responses=result.get_api_array_response(ApplicationApi.get_response_body_api()),
                         tags=['应用'])
    @has_permissions(PermissionConstants.APPLICATION_READ, compare=CompareConstants.AND)
    def get(self, request: Request):
        return result.success(
            ApplicationSerializer.Query(
                data={**query_params_to_single_dict(request.query_params), 'user_id': request.user.id}).list())

    class Operate(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['DELETE'], detail=False)
        @swagger_auto_schema(operation_summary="删除应用",
                             operation_id="删除应用",
                             manual_parameters=ApplicationApi.Operate.get_request_params_api(),
                             responses=result.get_default_response(),
                             tags=['应用'])
        @has_permissions(ViewPermission(
            [RoleConstants.ADMIN, RoleConstants.USER],
            [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.MANAGE,
                                            dynamic_tag=keywords.get('application_id'))],
            compare=CompareConstants.AND),
            lambda r, k: Permission(group=Group.APPLICATION, operate=Operate.DELETE,
                                    dynamic_tag=k.get('application_id')), compare=CompareConstants.AND)
        def delete(self, request: Request, application_id: str):
            return result.success(ApplicationSerializer.Operate(
                data={'application_id': application_id, 'user_id': request.user.id}).delete(
                with_valid=True))

        @action(methods=['PUT'], detail=False)
        @swagger_auto_schema(operation_summary="修改应用",
                             operation_id="修改应用",
                             manual_parameters=ApplicationApi.Operate.get_request_params_api(),
                             request_body=ApplicationApi.Create.get_request_body_api(),
                             responses=result.get_api_array_response(ApplicationApi.get_response_body_api()),
                             tags=['应用'])
        @has_permissions(ViewPermission(
            [RoleConstants.ADMIN, RoleConstants.USER],
            [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.USE,
                                            dynamic_tag=keywords.get('application_id'))],
            compare=CompareConstants.AND))
        def put(self, request: Request, application_id: str):
            return result.success(
                ApplicationSerializer.Operate(data={'application_id': application_id, 'user_id': request.user.id}).edit(
                    request.data))

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary="获取应用详情",
                             operation_id="获取应用详情",
                             manual_parameters=ApplicationApi.Operate.get_request_params_api(),
                             responses=result.get_api_array_response(ApplicationApi.get_response_body_api()),
                             tags=['应用'])
        @has_permissions(ViewPermission(
            [RoleConstants.ADMIN, RoleConstants.USER, RoleConstants.APPLICATION_ACCESS_TOKEN,
             RoleConstants.APPLICATION_KEY],
            [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.USE,
                                            dynamic_tag=keywords.get('application_id'))],
            compare=CompareConstants.AND))
        def get(self, request: Request, application_id: str):
            return result.success(ApplicationSerializer.Operate(
                data={'application_id': application_id, 'user_id': request.user.id}).one())

    class ListApplicationDataSet(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary="获取当前应用可使用的数据集",
                             operation_id="获取当前应用可使用的数据集",
                             manual_parameters=ApplicationApi.Operate.get_request_params_api(),
                             responses=result.get_api_array_response(DataSetSerializers.Query.get_response_body_api()),
                             tags=['应用'])
        @has_permissions(ViewPermission([RoleConstants.ADMIN, RoleConstants.USER],
                                        [lambda r, keywords: Permission(group=Group.APPLICATION, operate=Operate.USE,
                                                                        dynamic_tag=keywords.get('application_id'))],
                                        compare=CompareConstants.AND))
        def get(self, request: Request, application_id: str):
            return result.success(ApplicationSerializer.Operate(
                data={'application_id': application_id, 'user_id': request.user.id}).list_dataset())

    class Page(APIView):
        authentication_classes = [TokenAuth]

        @action(methods=['GET'], detail=False)
        @swagger_auto_schema(operation_summary="分页获取应用列表",
                             operation_id="分页获取应用列表",
                             manual_parameters=result.get_page_request_params(
                                 ApplicationApi.Query.get_request_params_api()),
                             responses=result.get_page_api_response(ApplicationApi.get_response_body_api()),
                             tags=['应用'])
        @has_permissions(PermissionConstants.APPLICATION_READ, compare=CompareConstants.AND)
        def get(self, request: Request, current_page: int, page_size: int):
            return result.success(
                ApplicationSerializer.Query(
                    data={**query_params_to_single_dict(request.query_params), 'user_id': request.user.id}).page(
                    current_page, page_size))