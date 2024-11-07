#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

class AliyunDNSUpdate():
    # 初始化
    # 传入AccessKey_ID、Access_Key_Secret 以及 region
    def __init__(self,AccessKey_ID :str,Access_Key_Secret :str,region :str):
        self._AccessKey_ID = AccessKey_ID
        self._Access_Key_Secret = Access_Key_Secret
        self._region = region
        self._Client = None

    # 登录
    def login(self) -> str:
        if None == self._Client:
            client = AcsClient(self._AccessKey_ID, self._Access_Key_Secret, self._region)
            self._Client = client
        return self._Client

    # 更新
    def update(self,recordID :str,domainValue :str,domainType :str,RR :str):
        client = self.login()
        try:
            request = UpdateDomainRecordRequest()
            request.set_accept_format('json')
            request.set_Value(domainValue)
            request.set_Type(domainType)
            request.set_RR(RR)
            request.set_RecordId(recordID)
            response = client.do_action_with_exception(request)
            
            logging.info("更新域名解析成功 %s",response)

        except Exception as e:
            logging.error("更新域名解析失败 %s",e)

    # 获取解析
    def recordDescribe(self,domainName :str):
        client = self.login()

        try:
            request = DescribeDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(domainName)
            response = client.do_action_with_exception(request)
            JsonDta = json.loads(str(response, encoding='utf-8'))
            return JsonDta["DomainRecords"]["Record"]
        except Exception as e:
            logging.error("获取[%s]域名解析失败: %s",domainName,e)
            return None