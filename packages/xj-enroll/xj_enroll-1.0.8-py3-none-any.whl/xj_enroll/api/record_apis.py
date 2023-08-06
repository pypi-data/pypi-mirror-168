from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from ..service.enroll_record_serivce import EnrollRecordServices
from ..utils.custom_response import util_response
from ..utils.model_handle import parse_data
from ..validator.record_validator import RecordValidator


class RecordAPI(APIView):
    # 添加记录,用户报名
    @require_http_methods(['POST'])
    def add(self, *args, **kwargs, ):
        params = parse_data(self)
        # 表单数据验证
        is_valid, error = RecordValidator(params).validate()
        if not is_valid:
            return util_response(err=1000, msg=error)
        # 添加数据
        data, err = EnrollRecordServices.record_add(params)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @require_http_methods(['GET'])
    def list(self, *args, **kwargs, ):
        params = parse_data(self)
        data, err = EnrollRecordServices.record_list(params=params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
