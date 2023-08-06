"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: CURD 工具
@created_time: 2022/9/15 14:14
"""

from django.core.paginator import Paginator, EmptyPage

from ..models import Enroll
from ..serializers import EnrollListSerializer
from ..utils.model_handle import format_params_handle


class EnrollServices:
    def __init__(self):
        pass

    @staticmethod
    def enroll_list(params):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id", "thread_id", "trading_relate", "region_code", "spend_time_start", "spend_time_end", "create_time_start", "create_time_end",
                "finish_time_start", "finish_time_end", "open_time_start", "open_time_end", "enroll_status_code", "bid_mode", "has_subitem"
            ],
            alias_dict={
                "spend_time_start": "spend_time__gte", "spend_time_end": "spend_time__lte", "create_time_start": "create_time__gte", "create_time_end": "create_time__lte",
                "finish_time_start": "finish_time__gte", "open_time_start": "open_time__gte", "open_time_end": "open_time__lte"
            }
        )
        enroll_obj = Enroll.objects.filter(**params).values()
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        res = EnrollListSerializer(enroll_obj, many=True)
        data = {'total': paginator.count, 'list': res.data}
        return data, None

    @staticmethod
    def enroll_detail(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, None
        enroll_detail = enroll_obj.first().to_json()
        return enroll_detail, None

    @staticmethod
    def enroll_edit(params, enroll_id):
        enroll_id = params.pop("enroll_id", None) or enroll_id
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "trading_relate", "region_code", "occupy_room", "enroll_status_code", "min_number", "max_number", "min_count_apiece", "max_count_apiece",
                "enroll_calc_rule_id", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount", "paid_amount", "unpaid_amount", "commision", "deposit",
                "bid_mode", "ticket", "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch", "need_deposit", "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time", "create_time", "update_time", "snapshot", "remark",
            ],
        )
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def enroll_delete(enroll_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return None, None
        try:
            enroll_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def enroll_add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "thread_id", "trading_relate", "region_code", "occupy_room", "enroll_status_code", "min_number", "max_number", "min_count_apiece", "max_count_apiece",
                "enroll_calc_rule_id", "price", "count", "unit", "fee", "reduction", "subitems_amount", "amount", "paid_amount", "unpaid_amount", "commision", "deposit",
                "bid_mode", "ticket", "hide_price", "hide_user", "has_repeat", "has_subitem", "has_audit", "has_vouch", "need_deposit", "need_imprest", "enable_pool",
                "pool_limit", "pool_stopwatch", "open_time", "close_time", "launch_time", "finish_time", "spend_time", "create_time", "update_time", "snapshot", "remark",
            ],
        )
        try:
            Enroll.objects.create(**params)
        except Exception as e:
            return None, str(e)

        return None, None
