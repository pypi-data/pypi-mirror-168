from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_enroll.service.enroll_services import EnrollServices
from xj_enroll.validator.enroll_validator import EnrollValidator
from ..utils.custom_response import util_response
from ..utils.model_handle import parse_data


class EnrollAPI(APIView):
    @require_http_methods(['GET'])
    def list(self, *args, **kwargs, ):
        params = parse_data(self)
        print("params:", params)
        data, err = EnrollServices.enroll_list(params=params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    def detail(self, *args, **kwargs, ):
        params = parse_data(self)
        enroll_id = kwargs.get("enroll_id") or params.pop("enroll_id") or None
        if not enroll_id:
            return util_response(err=1000, msg="参数错误:enroll_id不可以为空")
        data, err = EnrollServices.enroll_detail(enroll_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['POST'])
    def add(self, *args, **kwargs, ):
        params = parse_data(self)
        # 表单数据验证
        is_valid, error = EnrollValidator(params).validate()
        if not is_valid:
            return util_response(err=1000, msg=error)
        # 添加数据
        data, err = EnrollServices.enroll_add(params)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def edit(self, *args, **kwargs, ):
        params = parse_data(self)
        enroll_id = kwargs.get("enroll_id") or params.pop("enroll_id") or None
        if not enroll_id:
            return util_response(err=1000, msg="参数错误:enroll_id不可以为空")
        data, err = EnrollServices.enroll_edit(params, enroll_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['DELETE'])
    def delete(self, *args, **kwargs, ):
        params = parse_data(self)
        enroll_id = kwargs.get("enroll_id") or params.pop("enroll_id") or None
        if not enroll_id:
            return util_response(err=1000, msg="参数错误:enroll_id不可以为空")
        data, err = EnrollServices.enroll_delete(enroll_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
