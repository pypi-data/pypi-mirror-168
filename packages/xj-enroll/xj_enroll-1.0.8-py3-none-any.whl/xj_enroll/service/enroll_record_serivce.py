# encoding: utf-8
"""
@project: djangoModel->enroll_record_serivce
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户报名记录
@created_time: 2022/9/17 15:45
"""
from django.core.paginator import Paginator

from ..models import EnrollRecord
from ..utils.model_handle import format_params_handle


class EnrollRecordServices:

    @staticmethod
    def record_add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id",
                "enroll_id",
                "user_id",
                "enroll_auth_status_id",
                "enroll_pay_status_id",
                "enroll_status_code",
                "create_time",
                "price",
                "deposit",
                "count",
                "main_amount",
                "coupon_amount",
                "again_reduction",
                "subitems_amount",
                "deposit_amount",
                "amount",
                "paid_amount",
                "unpaid_amount",
                "fee",
                "photos",
                "files",
                "score",
                "reply",
                "remark",
            ],
        )
        try:
            EnrollRecord.objects.get_or_create(user_id=params["user_id"], enroll_id=params["enroll_id"], defaults=params)
        except Exception as e:
            return None, str(e)

        return None, None

    @staticmethod
    def record_list(params):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id",
                "enroll_id",
                "user_id",
                "enroll_auth_status_id",
                "enroll_pay_status_id",
                "enroll_status_code",
                "create_time",
                "price",
                "deposit",
                "count",
                "main_amount",
                "coupon_amount",
                "again_reduction",
                "subitems_amount",
                "deposit_amount",
                "amount",
                "paid_amount",
                "unpaid_amount",
                "fee",
                "photos",
                "files",
                "score",
                "reply",
                "remark",
            ],
        )
        enroll_obj = EnrollRecord.objects.filter(**params).values()
        count = enroll_obj.count()
        paginator = Paginator(enroll_obj, size)
        enroll_obj = paginator.page(page)
        enroll_list = list(enroll_obj.object_list)
        data = {'total': count, 'list': enroll_list}
        return data, None
