# 使用python实现修改阿里云DNS域名解析


## 安装依赖

```bash
pip3 install requests
pip3 install aliyun-python-sdk-core-v3
pip3 install aliyun-python-sdk-alidns==2.0.6
```



## 部署

```bash
git clone https://github.com/wangli2025/aliyunDnsUpdateRecord.git
cd aliyunDnsUpdateRecord
chmod +x main.py
sudo ln -s $(pwd)/main.py /usr/local/bin/aliyunDnsUpdateRecord
```



部署完成后，可以使用`aliyunDnsUpdateRecord --help` 查看帮助

```bash
$ aliyunDnsUpdateRecord --help
usage: aliyunDnsUpdateRecord [-h] [-c CONFIGPATH] [-d DOMAINNAME] [-r RR] [-t TYPE] [-v VALUE]

阿里云修改域名解析命令行工具

options:
  -h, --help            show this help message and exit
  -c CONFIGPATH, --configPath CONFIGPATH
                        配置文件
  -d DOMAINNAME, --DomainName DOMAINNAME
                        域名
  -r RR, --RR RR        主机
  -t TYPE, --Type TYPE  解析类型
  -v VALUE, --Value VALUE
                        解析值
$ 
```



## 使用

### 配置秘钥

#### 使用配置文件

```bash
cat .alidns.json
{
    "AliDNS_AccessKey_ID": "阿里云ID",
    "AliDNS_Access_Key_Secret": "阿里云key",
    "AliDNS_region_id": "区域"
}
```



#### 使用环境变量

```bash
export AliDNS_AccessKey_ID=阿里云ID
export AliDNS_Access_Key_Secret=阿里云key
export AliDNS_region_id=区域
```



秘钥读取顺序为：配置文件 --> 环境变量。**若读取到配置文件的内容了，则不会再获取环境变量配置。**



### 脚本执行



配置秘钥后，使用如下命令即可更新解析。

```bash
$ aliyunDnsUpdateRecord -d example.com -r www -t A -v 127.0.0.10
```





如果使用的是配置文件方式，且文件路径不是执行命令所在的`./.alidns.json`，则需要单独使用`-c` 单独指定。

```bash
$ cat c.json 
{
    "AliDNS_AccessKey_ID": "阿里云ID",
    "AliDNS_Access_Key_Secret": "阿里云key",
    "AliDNS_region_id": "区域"
}
$ 
$ aliyunDnsUpdateRecord -c c.json -d example.com -r www -t A -v 127.0.0.10
```



如果正确修改，会输入如下内容：

```bash
解析修改成功 example.com www 127.0.0.10
```



如果想将域名解析修改为本机所在的公网地址，则不用添加`-v` 即可。

```bash
$ aliyunDnsUpdateRecord -d example.com -r www -t A
```

如上默认会获取本机所在的公网地址，并且修改`example.com`的`www`主机上的`A`记录值。



### 报错信息

#### 秘钥配置出错

```bash
ERROR:root:获取[域名]域名解析失败: HTTP Status: 404 Error:InvalidAccessKeyId.NotFound Specified access key is not found. 
```



请检查秘钥配置是否正确。



#### 找不到域名

```bash
ERROR:root:获取[域名]域名解析失败: HTTP Status: 400 Error:InvalidDomainName.NoExist The specified domain name does not exist. Refresh the page and try again.
```



请检查域名配置是否正确。



#### RAM权限配置出错

```bash
ERROR:root:获取[域名]域名解析失败: HTTP Status: 403 Error:Forbidden.RAM User not authorized to operate on the specified resource, or this API doesn't support RAM. 
```



请检查RAM权限配置是否正确，如果没有配置更加细化的自定义策略，则应该添加 AliyunDNSFullAccess 系统策略。

#### 解析记录为找到

```bash
未找到该域名解析记录，请检查是否被添加，[域名信息]
```



未找到解析记录，请检查是否已经被添加了











