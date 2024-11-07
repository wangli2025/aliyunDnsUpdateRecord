#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import json
import aliyunDNSUpdateTools
import requests

# 从外网地址获取IIP
def getOutIP():

    headers = {"User-Agent": "curl/7.88.1"}
    urls = [
        "http://ipinfo1.io/ip",
        "http://ip.sb"
    ]

    for url in urls:
        try:
            r = requests.get(url,headers=headers)
            return r.text.strip()
        except Exception as e:
            print("get out ip error",e)
    else:
        return None
        

# 从配置文件或者是环境变量中加载阿里云key
def getConfig(configPath :str) -> dict:
    configDict = {}

    # 从配置文件中获取
    try:
        if os.path.exists(configPath):
            with open(configPath,"r") as f:
                jsonData = json.load(f)
            configDict["AliDNS_AccessKey_ID"] = jsonData["AliDNS_AccessKey_ID"]
            configDict["AliDNS_Access_Key_Secret"] = jsonData["AliDNS_Access_Key_Secret"]
            configDict["AliDNS_region_id"] = jsonData["AliDNS_region_id"]
            return configDict
    except Exception as e:
        pass

    # 从环境变量中获取
    try:
        AccessKey_ID = os.environ.get("AliDNS_AccessKey_ID")
        Access_Key_Secret = os.environ.get("AliDNS_Access_Key_Secret")
        region_id = os.environ.get("AliDNS_region_id")

        if AccessKey_ID == None or Access_Key_Secret == None or region_id == None:
            raise

        configDict["AliDNS_AccessKey_ID"] = AccessKey_ID
        configDict["AliDNS_Access_Key_Secret"] = Access_Key_Secret
        configDict["AliDNS_region_id"] = region_id

        return configDict
    except Exception as e:
        pass

    # 都获取失败，返回None
    return None

def main():
    parser = argparse.ArgumentParser(description="阿里云修改域名解析命令行工具")
    parser.add_argument('-c','--configPath',type=str,default="./.alidns1.json",help="配置文件")
    parser.add_argument('-d','--DomainName',type=str,help="域名")
    parser.add_argument('-r','--RR',type=str,help="主机")
    parser.add_argument('-t','--Type',type=str,default="A",help="解析类型")
    parser.add_argument('-v','--Value',default="outIP",type=str,help="解析值")

    args = parser.parse_args()

    if "outIP" == args.Value:
        outip = getOutIP()
        if outip == None:
            print("获取外网IP失败，请手动设置值")
            return
        args.Value = outip

    if args.DomainName == None or args.RR == None:
        print("参数不能为空，请检查 域名、主机")
        print("参照：python3 command.py -d 域名 -r 主机 -t 解析类型 -v 解析值")
        return

    if "outIP" == args.Value:
        pass

    config = getConfig(args.configPath)
    if config == None:
        print("加载阿里云秘钥失败，请检查配置文件或者环境变量配置是否正确。")
        return

    aliyunDnsClient = aliyunDNSUpdateTools.AliyunDNSUpdate(
        config["AliDNS_AccessKey_ID"],
        config["AliDNS_Access_Key_Secret"],
        config["AliDNS_region_id"])

    aliyunRecords = aliyunDnsClient.recordDescribe(args.DomainName)
    if None == aliyunRecords:
        return

    for aliyunRecord in aliyunRecords:
        if aliyunRecord["RR"] == args.RR and aliyunRecord["Type"] == args.Type:
            if args.Value == aliyunRecord["Value"]:
                print("待解析的值记录和目前aliyundns上一致")
            else:
                aliyunDnsClient.update(
                    aliyunRecord["RecordId"],
                    args.Value,
                    args.Type,
                    args.RR
                )
                print("解析修改成功",args.DomainName ,args.RR ,args.Value)

            break
    else:
        print("未找到该域名解析记录，请检查是否被添加，",args.DomainName,args.Type,args.RR)

if __name__ == "__main__":
    main()
