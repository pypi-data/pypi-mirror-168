# 温度填报

import requests
import datetime
import random

from .utils import Url, validate, ext_resubmit_flag, T_Response

prompt = {
    "success": "填报成功！",
    "refuse": "未在填报时间段（每天6点到20点）中，不能进行填报操作!",
    "has_report": "每次填报间隔时间应不能小于4小时!",
    "failed": ""
}
pattern = r"content.*?(?<=\')(.*?)(?=\')"


def _get_time_now():
    now = datetime.datetime.now()
    return now.hour, now.minute


def _build_tem_info():
    return int(36), random.randint(5, 9)


def _prep_req_data(**kwargs):
    time = _get_time_now()
    tem = _build_tem_info()
    return dict(TimeNowHour=str(time[0]),
                TimeNowMinute=str(time[1]),
                Temper1=str(tem[0]),
                Temper2=str(tem[1]),
                **kwargs)


@validate(prompts=prompt, pattern=pattern, proc_alias="the temperature sign-up")
def main(session: "requests.Session") -> T_Response:
    text = session.get(url=Url.TEM_INFO,
                       allow_redirects=False).text
    if isinstance(flag := ext_resubmit_flag(text), dict):
        flag = flag[0]
    data_ = _prep_req_data(ReSubmiteFlag=flag)

    resp = session.post(url=Url.TEM_INFO,
                        data=data_)
    return resp
