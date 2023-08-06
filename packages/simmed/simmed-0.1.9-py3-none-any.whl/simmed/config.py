import os

env = os.environ.get

# zipkin
ZIPKIN_HOST = env('ZIPKIN_HOST', 'localhost')  # 配置中心获取
ZIPKIN_PORT = env('ZIPKIN_PORT', 9411)
ZIPKIN_SAMPLE_RATE = env('ZIPKIN_SAMPLE_RATE', 100.0)
ZIPKIN_ENABLE = env('ZIPKIN_ENABLE', True)

# nacos
NACOS_ENABLE = env('NACOS_ENABLE', True)
DATA_ID = env('DATA_ID', 'specialdisease')
APPNAME = env('APPNAME', 'specialdisease')
APPDESC = env('APPDESC', '科研平台')
GROUP = env('GROUP', 'DEFAULT_GROUP')
NAMESPACE = env('NAMESPACE', '')  # 开发环境需要设置 local_dev
APP_ADDRESS = env('APP_ADDRESS', None)
NACOS_ADDRESS = env('NACOS_ADDRESS', 'localhost:8848')  # 通过环境变量获取

# flask
PORT = env('PORT', 5000)
FLASK_ENV = env('FLASK_ENV', 'local_dev')  # 通过环境变量获取，决定获取配置的组

# logs
LOG_ON = env('LOG_ON', True)
LOG_BY_MQ = env('LOG_BY_MQ', False)
LOG_LEVEL = env('LOG_LEVEL', 0)
