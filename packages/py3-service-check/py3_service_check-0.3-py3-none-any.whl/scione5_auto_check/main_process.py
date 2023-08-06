#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 1:49 下午
# @Author  : Meng Wang
# @Site    : 
# @File    : main_process.py
# @Software: PyCharm

from mysql_client import MysqlClient
import requests
import json
import uuid
from file_uploader import upload_file

stat_format = "=================%s=============================="

"""
检测程序主入口
"""

"""
检查数据库表是否创建成功
"""


def check_mysql():
    print(stat_format % "开始进入数据库自检程序")
    ip = input("请输入MySQL的IP")
    port = input("请输入MySQL的端口")
    username = input("请输入MySQL的账号")
    password = input("请输入MySQL的密码")
    print(stat_format % "开始进入数据库自检程序, 尝试建立建立连接")
    try:
        _mc = MysqlClient(ip=ip, port=port, username=username, password=password)
        print(stat_format % "数据库连接成功，检查数据库是否初始化完成")
        # 检查数据库是否存在
        results = _mc.query_by_sql("show databases")

        need_existed_dbs = ["analysis", "base", "hardware", "ilabservice-cloud-base",
                            "nacos", "offline_event_0", "offline_event_1", "ops_tsdb", "sale"]

        # 必须要的数据库
        env_type = input("请选择当前环境的类型：1000监控保,  0100仪器保, 0010库存保，依次类推")
        for i in range(0, len(env_type)):
            c = env_type[i]
            if c == '1':
                if i == 0:
                    need_existed_dbs.append("monitor")
                if i == 1:
                    need_existed_dbs.append("asset")
                if i == 2:
                    need_existed_dbs.append("inventory")

        # 当前环境中存在的
        current_dbs = []
        for result in results:
            current_dbs.append(result["Database"])
        for i in need_existed_dbs:
            if i not in current_dbs:
                print(stat_format % ("数据库匹配失败，存在未初始化的数据库 : " + i))
                exec("")
        print(stat_format % "数据库匹配完成, 数据库检查完毕，开始检查基础数据 t_service")

        # 检查t_service数据
        _mc2 = MysqlClient(ip=ip, port=port, username=username, password=password, db_name="ilabservice-cloud-base")
        results2 = _mc2.query_by_sql("select * from t_service")

        if results2 is None or len(results2) < 5:
            print(stat_format % ("当前环境基础数据有误，ilabservice-cloud-base.t_service数据缺失!!!"))
            exec("")

        """
        查询初始产品包, 如果是本地部署，需要将产品包的icon上传至本地oss
        """
        print(stat_format % ("开始进入产品包的初始化工作中"))
        _saledb = MysqlClient(ip=ip, port=port, username=username, password=password, db_name="sale")
        pkg_res = _saledb.query_by_sql("select * from t_product_package")
        if pkg_res is None or len(pkg_res) == 0:
            print(stat_format % ("产品包初始化为空，请初始化产品包"))
            exec("")

        is_local = int(input("是否是本地部署用户， 0不是  1是"))
        if is_local == 1:
            # 产品包icon需要上传到oss上面
            from file_uploader_v2 import upload
            for pkg in pkg_res:
                url = pkg["icon_url"]
                if url is not None:
                    _id = pkg["id"]





    except Exception as error:
        print(stat_format % "数据库连接失败，自检程序结束！！！")
        exec("")


def service_check_api(url, service_name, standard):
    try:
        res_txt = requests.get(url=url).text
        print(stat_format % "服务健康状态返回：{}".format(res_txt))
        res_json = json.loads(res_txt)
        # 是否是标准健康检查
        if standard is False:
            if "success" in res_json and res_json["success"] is True:
                pass
            else:
                # 服务健康检查失败
                print(stat_format % "{}健康检查失败，自检程序结束！！！".format(service_name))
                exit(1)
        else:
            if "status" in res_json and res_json["status"] == "up":
                pass
            else:
                print(stat_format % "{}健康检查失败，自检程序结束！！！".format(service_name))
                exit(1)

    except Exception as e:
        print(stat_format % "{}连接失败，自检程序结束！！！".format(service_name))
        exit(1)


"""
检查服务状态
"""


def check_service():
    print(stat_format % "开始进入服务状态自检程序")
    ###############---------------------以下是基础服务组件检查---------------------------------------###########
    base_url = input("请输入基础服务的入口地址  如：http://192.168.100.233")

    service_check_api(base_url + "/api/base/sso/login", "cloud-base", False)

    service_check_api(base_url + "/api/labbase/service/health", "lab-general", True)

    service_check_api(base_url + "/api/hardware/service/health", "lab-hardware", True)

    service_check_api(base_url + "/api/sale/service/health", "lab-sale", True)
    ###############---------------------以上是基础服务组件检查---------------------------------------###########

    monitor_check = int(input("监控保服务是否检查 0:不检查 1检查"))
    if monitor_check == 1:
        # 检查监控保服务状态
        service_check_api(base_url + "/api/monitor/service/health", "lab-monitor", True)
        service_check_api(base_url + ":10060/service/health", "message", True)
        service_check_api(base_url + ":9012/service/health", "connector", True)
        service_check_api(base_url + ":9011/service/health", "diagram-processor", True)
        """
            是否需要DTU
        """
        dtu_need = int(input("是否需要DTU 0:不需要 1需要"))
        if dtu_need == 1:
            service_check_api(base_url + ":9997/agent/service/health", "agent-service", True)

    asset_check = int(input("仪器保服务是否检查 0:不检查 1检查"))
    if asset_check == 1:
        service_check_api(base_url + "/api/asset/service/health", "lab-asset", True)

    asset_check = int(input("库存保服务是否检查 0:不检查 1检查"))
    if asset_check == 1:
        service_check_api(base_url + "/api/inventory/service/health", "lab-inventory", True)

    print(stat_format % "完成微服务健康状态自检程序")


def api_test_assert(url, access_token, api_name, method, json_data):
    headers = {
        "Authorization": "Bearer " + access_token
    }
    try:
        res = requests.request(method=method, url=url, headers=headers, json=json_data).text
        print(stat_format % "接口请求结果：{}".format(res))
        res_json = json.loads(res)
        if "success" in res_json and res_json["success"] is True:
            pass

        else:
            print(stat_format % "接口请求失败, success is False：{}".format(api_name))
            exec("")

    except Exception as e:
        print(stat_format % "接口请求失败：{}".format(api_name))
        exec("")


def random_str(prefix):
    return prefix + "-" + str(uuid.uuid4())[0:8]


def random_email():
    return str(uuid.uuid4())[0:8] + "@163.com"


# 生成默认设备分类 这个接口估计要三分钟
def init_device_category(headers, url, saas_org_id):
    print(stat_format % "开始生成默认的设备分类")
    try:
        data_ = {
            "orgId": str(saas_org_id)
        }
        res = requests.post(url=url, headers=headers, timeout=180, json=data_).text
        print(stat_format % "生成默认的设备分类结果为：{}".format(res))
        res_dict = json.loads(res)
        if not res_dict["success"]:
            print(stat_format % "生成默认的设备分类失败")
            exec
    except Exception as e:
        print(stat_format % "生成默认的设备分类失败")
        exec

    print(stat_format % "生成默认的设备分类结束")


"""
自动化测试CRM
"""


def auto_test_crm():
    print(stat_format % "开始进入CRM的自动化测试程序")
    crm_url = input("请输入CRM的链接地址，如：http://192.168.100.233:81")

    print(stat_format % "开始进入CRM登录程序")

    data = {
        "appId": "611104697126f335578ac201",
        "loginType": "PASSWORD",
        "orgId": '1',
        "password": "EfqbL7ShMCLwG9msK/Zenw==",
        "username": "ilabservice"
    }

    access_token = ""
    try:
        login_res = requests.post(url=crm_url + "/api/labbase/v1/auth/login/account", json=data).text
        login_res_json = json.loads(login_res)
        if "success" in login_res_json and login_res_json["success"] is True:
            access_token = login_res_json["data"]["accessToken"]
        if access_token == "":
            print(stat_format % "CRM登录失败, 获取token失败")
            exit(1)
    except Exception as e:
        print(stat_format % "CRM登录失败")
        exit(1)

    """
    新增客户
    """
    saas_name = random_str("company")
    saas_admin_name = random_str("admin_user")
    saas_telephone = input("请输入客户手机号，如：13412345678")
    saas_email = random_email()

    add_saas_company = {
        "province": "北京市",
        "city": "北京市",
        "name": saas_name,
        "shortName": random_str("short"),
        "serviceStatus": 1,
        "environmentStatus": "合同",
        "industry": "99",
        "parentId": 1,
        "operationManager": random_str("operationManager")[3:7],
        "managerName": saas_admin_name,
        "managerPhone": saas_telephone,
        "email": saas_email,
        "address": random_str("address"),
        "telephone": saas_telephone,
        "type": "SaaS",
        "orgId": "1"
    }

    api_test_assert(url=crm_url + "/api/labbase/v1/company/secure/add", access_token=access_token, api_name="新增SAAS企业",
                    json_data=add_saas_company, method="POST")

    print(stat_format % "企业生成成功，用户名为：{}, 密码为Aa-123456".format(saas_telephone))

    # 新增合同 1. 先查询所有公司
    query_saas_list_url = crm_url + "/api/labbase/v1/secure/crm/all?orgId=1"
    headers = {
        "Authorization": "Bearer " + access_token
    }

    saas_org_id = 0
    try:
        query_res = json.loads(requests.get(url=query_saas_list_url, headers=headers).text)
        for item in query_res["data"]:
            saas_org_id = item["key"]
            break
    except Exception as e:
        print(stat_format % "企业查询失败")
        exec("")

    add_contract_body = {
        "sysNo": random_str("sysNo"),
        "companyId": str(saas_org_id),
        "type": "1",
        "startTime": 1654185600000,
        "contractPeriod": 24,
        "deployTime": 1656604800000,
        "acceptanceTime": 1656691200000,
        "endTime": 1719935999999,
        "warrantyPeriod": 12,
        "warrantStartTime": 1656691200000,
        "warrantEndTime": 1688313599999,
        "deployType": 3,
        "saleDirector": "zhu",
        "signatory": "zhu",
        "installer": "zhu",
        "afterSales": "zhu",
        "id": "",
        "validDay": 0,
        "orgId": "1"
    }

    api_test_assert(url=crm_url + "/api/sale/v1/secure/contract", access_token=access_token, api_name="新增合同",
                    json_data=add_contract_body, method="POST")

    print(stat_format % "企业合同创建成功")

    # 查询最新合同
    query_contract_url = crm_url + "/api/sale/v1/secure/contract/list?pageNum=1&pageSize=10&orgId=1"
    contract_id = 0
    try:
        query_c_res = json.loads(requests.get(url=query_contract_url, headers=headers).text)
        for item in query_c_res["data"]["records"]:
            contract_id = item["id"]
            break
    except Exception as e:
        print(stat_format % "合同列表查询失败")
        exec("")

    # 合同内新增产品包
    add_pkg_url = crm_url + "/api/sale/v1/secure/contract/{}/pkg/batch?orgId=1".format(contract_id)
    add_pkg_body = [
        {
            "productPackageOrderId": 94,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 93,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 92,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 91,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 90,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 89,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 88,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 87,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 84,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 83,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 82,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 81,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 80,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 79,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 78,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 77,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 76,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 75,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 74,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 73,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 72,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 69,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 68,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 67,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 66,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 65,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 64,
            "timeCount": 1,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 63,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 51,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 50,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 49,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 48,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 47,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 46,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 45,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 44,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 43,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 42,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 41,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 40,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 39,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 38,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 37,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 36,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 35,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 34,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 33,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 32,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 31,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 30,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 29,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 28,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 27,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 26,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 25,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 24,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 23,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 22,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 21,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 20,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 19,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 18,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 17,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 16,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 15,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 14,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 13,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 12,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 11,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 10,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 9,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 8,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 7,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 6,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 5,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 4,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 3,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 2,
            "timeCount": None,
            "pkgCount": 1
        },
        {
            "productPackageOrderId": 1,
            "timeCount": None,
            "pkgCount": 1
        }
    ]

    api_test_assert(url=add_pkg_url, access_token=access_token, api_name="合同中新增产品包", json_data=add_pkg_body,
                    method="POST")

    print(stat_format % "合同产品包配置成功")

    print(stat_format % "CRM自动测试程序结束，请用{}登录".format(saas_telephone))

    # 开始测试saas
    auto_saas_test(saas_telephone, saas_org_id)


def upload_file_test(access_token, upload_url, saas_org_id):
    succeed = upload_file(access_token=access_token, org_id=saas_org_id, upload_url=upload_url)
    if succeed is None:
        print(stat_format % "文件上传失败")
        exit("")
    return succeed


# 查询设备类型编号
def query_category_id(headers, url, saas_org_id):
    print(stat_format % "开始查询设备类型编号")
    try:
        res = requests.get(url=url + "?orgId={}".format(saas_org_id), headers=headers).text
        res_dict = json.loads(res)
        ids = []
        for item in res_dict["data"]:
            ids.append(item["id"])
            for itemc in item["children"]:
                ids.append(itemc["id"])
                for itemb in itemc["children"]:
                    ids.append(itemb["id"])
                    break
                break
            break
        return ids
    except Exception as e:
        print(stat_format % "查询品牌列表失败！！！")
        exec


def query_qdwy_brand_id(headers, url, saas_org_id):
    # 查询青岛伟业的品牌id
    print(stat_format % "开始查询品牌列表")
    try:
        res = requests.get(url=url + "?orgId={}".format(saas_org_id), headers=headers).text
        res_dict = json.loads(res)
        for item in res_dict["data"]:
            if item["name"] == "青岛动力伟业":
                return item["id"]
    except Exception as e:
        print(stat_format % "查询品牌列表失败！！！")
        exec


def query_model_id_by_brand(headers, brand_id, saas_org_id, url):
    print(stat_format % "开始查询品牌对应的型号列表")
    try:
        res = requests.get(url=url + "?brandId={}&orgId={}".format(brand_id, saas_org_id), headers=headers).text
        res_dict = json.loads(res)
        for item in res_dict["data"]:
            return item["id"]
    except Exception as e:
        print(stat_format % "查询品牌列表失败！！！")
        exec


def auto_saas_test(telephone, saas_org_id):
    saas_base_url = input("请输入SAAS的链接地址，如：http://192.168.100.233")
    # 开始登录
    saas_login_url = saas_base_url + "/api/labbase/v1/auth/login/account"
    # 默认密码Aa-123456
    login_data = {
        "username": telephone,
        "password": "cB6RZfrLZIh1+LVNc+RveA==",
        "loginType": "PASSWORD",
        "appId": "611104697126f335578ac201",
        "orgId": saas_org_id
    }

    saas_access_token = ""
    try:
        login_res = requests.post(url=saas_login_url, json=login_data).text
        login_res_json = json.loads(login_res)
        if "success" in login_res_json and login_res_json["success"] is True:
            saas_access_token = login_res_json["data"]["accessToken"]
        if saas_access_token == "":
            print(stat_format % "SAAS登录失败, 获取token失败")
            exit("")
    except Exception as e:
        print(stat_format % "SAAS登录失败")
        exit("")

    headers = {
        "Authorization": "Bearer " + saas_access_token
    }
    is_local = int(input("是否是本地部署用户， 0不是  1是"))
    # 获取配置的保的地址是否合理
    query_domain_url = saas_base_url + "/api/labbase/v1/system/app/domain?orgId={}".format(saas_org_id)

    try:
        rs = json.loads(requests.get(url=query_domain_url, headers=headers).text)
        if rs["success"]:
            domain_data = rs["data"]
            for key, value in domain_data.items():
                # 如果配置的不对，报错
                if saas_base_url not in value:
                    print(stat_format % "业务系统主页配置有误！{} 配置的是 {}".format(key, value))
                    exit("")
    except Exception as e:
        print(stat_format % "获取SAAS的域名配置失败！")
        exit("")

    file_url = upload_file_test(access_token=saas_access_token,
                                upload_url=saas_base_url + "/api/labbase/v1/secure/oss/uploadfile",
                                saas_org_id=saas_org_id)
    # 上传图片 看看是否配置对不对
    if is_local == 1:
        # 本地部署 需要校验
        if saas_base_url not in file_url:
            # 本地文件上传部署有问题
            print(stat_format % "文件上传显示有误，应该是上传至Minio，现在上传到别的地方, 文件URL : {}".format(file_url))
            exit("")

    # 新增房间
    data = {
        "siteName": random_str("d"),
        "buildName": "1",
        "floorName": "101",
        "roomName": "101",
        "plabType": "无",
        "gxpType": 9,
        "functionIntro": "",
        "assetPhoto": file_url,
        "testItems": [],
        "orgId": str(saas_org_id)
    }
    api_test_assert(url=saas_base_url + "/api/labbase/v1/secure/location/add", access_token=saas_access_token,
                    api_name="新增房间", method="POST", json_data=data)

    # 查询房间
    query_room_url = saas_base_url + "/api/labbase/v1/secure/location/page?pageSize=10&pageNum=1&orgId={}".format(
        saas_org_id)

    room_location_id = 0
    try:
        room_res_txt = requests.get(url=query_room_url, headers=headers).text
        print(stat_format % "房间列表返回：{}".format(room_res_txt))
        room_res = json.loads(room_res_txt)
        if room_res["success"] and "data" in room_res:
            data_obj = room_res["data"]
            for record in data_obj["records"]:
                room_location_id = record["locationId"]
                break
    except Exception as e:
        print(stat_format % "新增房间失败")
        print(e)
        exit("")

    if room_location_id == 0:
        print(stat_format % "新增房间失败[room 返回为空]")
        exit("")

    # 默认的设备分类初始化
    init_device_category(headers=headers, url=saas_base_url + "/api/base/v1/secure/asset/category/init",
                         saas_org_id=saas_org_id)

    # 新增设备
    brand_id = query_qdwy_brand_id(headers=headers,
                                   url=saas_base_url + "/api/labbase/v1/secure/devicedetail/brand/template",
                                   saas_org_id=saas_org_id)
    category_ids = query_category_id(headers=headers,
                                     url=saas_base_url + "/api/labbase/v1/secure/devicedetail/category",
                                     saas_org_id=saas_org_id)
    add_device_data = {
        "asset_number": random_str("ano"),
        "name": random_str("dname"),
        "assetTypeId": category_ids,
        "asset_brand_id": brand_id,
        "asset_brand_model_id": query_model_id_by_brand(headers=headers, brand_id=brand_id, saas_org_id=saas_org_id,
                                                        url=saas_base_url + "/api/labbase/v1/secure/devicedetail/model/template"),
        "status": "1",
        "location_id": room_location_id,
        "first_asset_category_id": category_ids[0],
        "second_asset_category_id": category_ids[1],
        "asset_category_id": category_ids[2],
        "orgId": str(saas_org_id)
    }
    api_test_assert(url=saas_base_url + "/api/labbase/v1/secure/labassets/add", access_token=saas_access_token,
                    api_name="新增设备", method="POST", json_data=add_device_data)

    print(stat_format % "SAAS系统自检结束，已完成当前检查")


def run_main():
    check_mysql()
    check_service()
    auto_test_crm()


if __name__ == '__main__':
    run_main()
