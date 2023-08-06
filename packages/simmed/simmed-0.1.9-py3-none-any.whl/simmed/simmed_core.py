import hashlib
from itertools import groupby
import json
from operator import itemgetter
import random
from flask import request, g
from flask_compress import Compress
from flask_cors import CORS
from flasgger import Swagger
import requests
from simmed.zipkin import flask_start_zipkin, flask_stop_zipkin, set_tags, with_zipkin_request
from simmed.jsonencoder import Flask
from datetime import datetime

import logging
import simmed.nacos_client as nacos_client
import simmed.config as config


def init_flask_app():
    """
    初始化
    init: app, compress, nacos, zipkin, config
    Returns:
        _type_: flask app
    """

    app = Flask(__name__, static_folder="static",
                static_url_path="/static", template_folder="templates")

    app.config['COMPRESS_MIN_SIZE'] = 0
    Compress(app)

    Swagger(app)
    # print(app.root_path)
    # print(app.static_folder)
    # print(app.template_folder)
    CORS(app, supports_credentials=True)
    nacos_client.regis_server_to_nacos(app)

    nacos_config = get_config("")
    if nacos_config:
        if 'ZIPKIN_HOST' in nacos_config:
            config.ZIPKIN_HOST = str(nacos_config['ZIPKIN_HOST'])
        if 'ZIPKIN_PORT' in nacos_config:
            config.ZIPKIN_PORT = int(nacos_config['ZIPKIN_PORT'])
        if 'ZIPKIN_SAMPLE_RATE' in nacos_config:
            config.ZIPKIN_SAMPLE_RATE = float(
                nacos_config['ZIPKIN_SAMPLE_RATE'])
        if 'ZIPKIN_ENABLE' in nacos_config:
            config.ZIPKIN_ENABLE = bool(nacos_config['ZIPKIN_ENABLE'])

    @app.route("/heartbeat", methods=['GET'])
    def heartbeat():
        """
        心跳
        ---
        tags: ['系统']
        responses:
            200:
                description: 成功返回 ok
        """
        return "ok"

    @app.route("/generateDoc", methods=['GET'])
    def generateDoc():
        """
        生成文档
        ---
        tags: ['系统']
        responses:
            200:
                description: 成功返回 True
        """
        file_path = "apispec_1.json"
        try:
            url = request.host_url+file_path
            result = requests.get(url).text
            swagger = json.loads(result)

        except Exception as ex:
            print(ex)

        apidoc = {
            "ModuleName": "SpecialDisease",
            "ModuleText": "临床科研",
            "ModuleUrl": "api/v0.1/{controller}",
            "Services": []
        }

        apis = []
        i = 0

        for path in swagger['paths']:
            service = swagger['paths'][path]
            for method in service:
                parameters = []
                if 'parameters' in service[method]:
                    params = service[method]['parameters']
                    for param in params:
                        param_in = param['in']
                        if param_in == "path" or param_in == "formData" or param_in == "query":
                            parameters.append({
                                "MaxLength": 0,
                                "Name":  param['name'],
                                # "In": param_in,
                                "Text":  param['description'] if "description" in param else '',
                                "TypeName": param['type'] if "type" in param else '',
                                "Nullable":  "否" if 'required' in param and param['required'] else "是",
                                # "Properties": []
                            })
                        else:
                            if 'schema' in param:
                                schema = param['schema']
                                if 'properties' in schema and schema['properties']:
                                    for proname in schema['properties']:
                                        typename = schema['properties'][proname]['type'] if "type" in schema['properties'][proname] else ''
                                        parameter = {
                                            "MaxLength": 0,
                                            "Name":  proname,
                                            # "In": param_in,
                                            "Text":  schema['properties'][proname]['description'] if "description" in schema['properties'][proname] else '',
                                            "TypeName": schema['properties'][proname]['type'] if "type" in schema['properties'][proname] else '',
                                            "Nullable":  "否" if 'required' in schema and schema['required'] and proname in schema['required'] else "是",
                                            # "Properties": []
                                        }
                                        if typename == "object" or typename == "array":
                                            # parameter['Properties'] = []
                                            i += 1
                                        parameters.append(parameter)

                m2 = hashlib.md5()
                m2.update((path+method).encode("utf8"))
                apiId = m2.hexdigest()

                hasPathParams = 1 if '{' in path else 0
                path = path.replace("/api/v0.1/", "")
                if hasPathParams == 1:
                    path = path[0:path.index('{')]+'**'

                apis.append({
                    "ServiceName": path,
                    "ServiceText": service[method]['tags'][0],
                    "Id": apiId,
                    "ApiName": method,
                    "ApiText": service[method]['summary'],
                    "HasPathParams": hasPathParams,
                    "RpcCheck": 0,
                    "LoginCheck": 1,
                    "NeedLogin": "是",
                    "Obsolete": False,
                    "ParentId": "0",
                    "OutputParams": {
                        "Name": "Result",
                        "Text": "Object",
                        "TypeName": "Object"
                    },
                    "InputParams": parameters
                })

        apis.sort(key=itemgetter('ServiceName'))
        for ServiceName, items in groupby(apis, key=itemgetter('ServiceName')):
            svcItems = []
            serviceText = ''
            for item in items:
                serviceText = item['ServiceText']
                svcItems.append({
                    "Id": item['Id'],
                    "ApiName": item['ApiName'],
                    "ApiText": item['ApiText'],
                    # "RpcCheck": item['RpcCheck'],
                    "LoginCheck": item['LoginCheck'],
                    "NeedLogin": item['NeedLogin'],
                    # "Obsolete": item['Obsolete'],
                    # "ParentId": item['ParentId'],
                    # "OutputParams": item['OutputParams'],
                    # "InputParams": item['InputParams']
                })

            m5 = hashlib.md5()
            m5.update(ServiceName.encode("utf8"))
            serviceId = m5.hexdigest()

            apidoc["Services"].append({
                "Id": serviceId,
                "ServiceName": ServiceName,
                "ServiceText": serviceText,
                "Apis": svcItems
            })

        result = rpc_rest_service("doc", "/api/doc/module", "Save", apidoc)
        print(result)
        return "success"

    @app.before_request
    def before():
        """
        针对app实例定义全局拦截器,开始请求
        """
        flask_start_zipkin()
        # print(request.endpoint)
        if request.endpoint != 'static':
            requestCorpId = request.headers['request-corpid'] if 'request-corpid' in request.headers else ''
            weAppAuthorization = request.headers['weappauthorization'] if 'weappauthorization' in request.headers else ''
            clientName = request.headers['User-Agent'] if 'User-Agent' in request.headers else ''
            browserInfo = clientName.split('/')[0]
            set_zipkin_tags({
                "http.url":  str(request.url),
                "http.host":  str(request.host),
                "http.path": str(request.path),
                "req.requestCorpId": requestCorpId,
                "req.weAppAuthorization": weAppAuthorization,
                "req.clientName": clientName,
                "req.content.type": str(request.content_type),
                "req.method": str(request.method),
                "req.endpoint": str(request.endpoint),
                "req.client": str(request.remote_addr)
            })
            audit_info = {
                "ClientRequestId": str(request.args['ClientRequestId']) if 'ClientRequestId' in request.args else None,
                "BaseClientRequestId": str(
                    request.args['BaseClientRequestId']) if 'BaseClientRequestId' in request.args else None,
                "RequestCorpId": requestCorpId,
                "AppId": str(request.args['AppId']) if 'AppId' in request.args else None,
                "ActionUrl": str(request.url),
                "ModuleName": config.APPNAME,
                "ActionName": str(request.method),
                "ServiceName": config.APPNAME,
                "MethodName": str(request.endpoint),
                "Parameters": str(request.data, 'utf8'),
                "BeginTime": datetime.now(),
                "ClientIpAddress": str(request.remote_addr),
                "ClientName": clientName,
                "BrowserInfo": browserInfo,
                "HasException": False
            }
            span = g.get('_zipkin_span')
            if span and span.zipkin_attrs:
                audit_info['ParentSpanId'] = span.zipkin_attrs.parent_span_id
                audit_info['SpanId'] = span.zipkin_attrs.span_id
                audit_info['TraceId'] = span.zipkin_attrs.trace_id
                audit_info['Sampled'] = span.zipkin_attrs.is_sampled
            g._audit_info = audit_info
        pass

    @app.after_request
    def after(response):
        """
        针对app实例定义全局拦截器,有异常不支持
        """
        # print(request.endpoint)
        if request.endpoint != 'static' and response.content_type in ['text/html', 'text/xml', 'application/json']:
            if str(request.method).lower() == "post":
                logging.debug("api response: %s",
                              str(response.data, 'utf8'))
            audit_info = g.get('_audit_info')
            audit_info['Output'] = str(response.data, 'utf8')
        return response

    @app.teardown_request
    def teardown(exception):
        """
        针对app实例定义全局拦截器,忽略异常
        """
        print(exception)
        print(request.endpoint)
        audit_info = g.get('_audit_info')
        if audit_info is not None:
            audit_info['EndTime'] = datetime.now()
            duration = audit_info['EndTime'] - audit_info['BeginTime']
            audit_info['ExecutionDuration'] = duration.microseconds
            if exception:
                logging.exception("api exception: %s", str(exception))
                set_zipkin_tags({
                    "req.headers": str(request.headers).rstrip(),
                    "req.form": json.dumps(request.form),
                    "req.exception": str(exception)
                })
                audit_info['HasException'] = True
                audit_info['Exception'] = str(exception)
            log_save('AuditInfo', json.dumps(
                audit_info, ensure_ascii=False, indent=4, sort_keys=True, default=str))
        flask_stop_zipkin()
        pass

    return app


def set_zipkin_tags(tag):
    """_summary_
    保存zipkin链路标签日志
    Args:
        tag (_type_): dict()
    """
    set_tags(tag)


def get_config(env_name):
    """
    从nacos配置中心获取配置
    Args:
        env_name (_type_): 环境, 如: local_dev

    Returns:
        _type_: json object
    """
    if not env_name:
        env_name = config.FLASK_ENV
    return nacos_client.get_config(env_name)


def rpc_rest_service(service_name, api, method, *params):
    """
    服务rpc公共方法
    Returns:
        _type_: 1.json object, 2.error string
    """
    headers = {
        'Content-Type': 'application/json'
    }
    requests_json = {
        "id": str(random.randint(10000, 99999)),
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    }

    set_zipkin_tags({
        "rpc.{}.api".format(requests_json["id"]): api,
        "rpc.{}.serviceName".format(requests_json["id"]): service_name,
        "rpc.{}.method".format(requests_json["id"]): method
    })

    host = nacos_client.get_service_host(service_name)
    if not host:
        set_zipkin_tags({
            "rpc.{}.error".format(requests_json["id"]): "注册中心未找到服务实例!"
        })
        return None

    set_zipkin_tags({
        "rpc.{}.host".format(requests_json["id"]): host
    })
    body = json.dumps(requests_json, ensure_ascii=False,
                      indent=4, sort_keys=True, default=str)
    logging.debug("request:" + body)

    try:
        def func(req_headers):
            return requests.post(
                "http://{}{}".format(host, api), headers=req_headers,  data=body.encode("utf-8"))

        response = with_zipkin_request(func, headers)
        rsp_text = response.text
        result = json.loads(rsp_text.encode('utf8'))

        logging.debug("response:" + rsp_text)

        if result:
            if result["code"] == 0 and "result" in result and result["result"]:
                return result["result"], None
            else:
                return None, result["message"]

        return None, None

    except Exception as ex:

        logging.exception("rpc exception:"+str(ex))
        set_zipkin_tags({
            "rpc.{}.params".format(requests_json["id"]): body if body else "None",
            "rpc.{}.exception".format(requests_json["id"]): str(ex)
        })
        return None, str(ex)


def log_save(logtype, logstr):
    if not config.LOG_ON:
        return

    if config.LOG_BY_MQ:
        '''
        通过MQ发送日志,待完善...
        '''
        pass
    else:
        rpc_rest_service("logs", "/api/logs/logsave", "SaveToMQ", json.dumps({
            "logType": logtype,
            "logStr": logstr
        }, ensure_ascii=False))


class Log:
    """
    日志记录
    Trace 0,Debug 1,Information 2,Warning 3,Error 4,Critical 5
    """

    def trace(self, logstr):
        if config.LOG_LEVEL <= 0:
            log_save("Trace", logstr)

    def debug(self, logstr):
        if config.LOG_LEVEL <= 1:
            log_save("Debug", logstr)

    def info(self, logstr):
        if config.LOG_LEVEL <= 2:
            log_save("Information", logstr)

    def warning(self, logstr):
        if config.LOG_LEVEL <= 3:
            log_save("Warning", logstr)

    def error(self, logstr):
        if config.LOG_LEVEL <= 4:
            log_save("Error", logstr)

    def critical(self, logstr):
        if config.LOG_LEVEL <= 5:
            log_save("Critical", logstr)


log = Log()
