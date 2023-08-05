import abc   # 利用abc模块实现抽象类
import json
from urllib.parse import unquote


class HttpBase:
    http_status_code = {
        # 1** 信息，服务器收到请求，需要请求者继续执行操作
        100: "100 Continue",  # 继续。客户端应继续其请求
        101: "101 Switching Protocols",  # 切换协议。服务器根据客户端的请求切换协议。只能切换到更高级的协议，例如，切换到HTTP的新版本协议
        # 2** 成功，操作被成功接收并处理
        200: "200 OK",  # 请求成功。一般用于GET与POST请求
        201: "201 Created",  # 已创建。成功请求并创建了新的资源
        202: "202 Accepted",  # 已接受。已经接受请求，但未处理完成
        203: "203 Non-Authoritative Information",  # 非授权信息。请求成功。但返回的meta信息不在原始的服务器，而是一个副本
        204: "204 No Content",  # 无内容。服务器成功处理，但未返回内容。在未更新网页的情况下，可确保浏览器继续显示当前文档
        205: "205 Reset Content",  # 重置内容。服务器处理成功，用户终端（例如：浏览器）应重置文档视图。可通过此返回码清除浏览器的表单域
        206: "206 Partial Content",  # 部分内容。服务器成功处理了部分GET请求
        # 3** 重定向，需要进一步的操作以完成请求
        300: "300 Multiple Choices",  # 多种选择。请求的资源可包括多个位置，相应可返回一个资源特征与地址的列表用于用户终端（例如：浏览器）选择
        301: "301 Moved Permanently",  # 永久移动。请求的资源已被永久的移动到新URI，返回信息会包括新的URI，浏览器会自动定向到新URI。今后任何新的请求都应使用新的URI代替
        302: "302 Found",  # 临时移动。与301类似。但资源只是临时被移动。客户端应继续使用原有URI
        303: "303 See Other",  # 查看其它地址。与301类似。使用GET和POST请求查看
        304: "304 Not Modified",  # 未修改。所请求的资源未修改，服务器返回此状态码时，不会返回任何资源。客户端通常会缓存访问过的资源，通过提供一个头信息指出客户端希望只返回在指定日期之后修改的资源
        305: "305 Use Proxy",  # 使用代理。所请求的资源必须通过代理访问
        306: "306 Unused",  # 已经被废弃的HTTP状态码
        307: "307 Temporary Redirect",  # 临时重定向。与302类似。使用GET请求重定向
        # 4** 客户端错误，请求包含语法错误或无法完成请求
        400: "400 Bad Request",  # 客户端请求的语法错误，服务器无法理解
        401: "401 Unauthorized",  # 请求要求用户的身份认证
        402: "402 Payment Required",  # 保留，将来使用
        403: "403 Forbidden",  # 服务器理解请求客户端的请求，但是拒绝执行此请求
        404: "404 Not Found",  # 服务器无法根据客户端的请求找到资源（网页）。通过此代码，网站设计人员可设置"您所请求的资源无法找到"的个性页面
        405: "405 Method Not Allowed",  # 客户端请求中的方法被禁止
        406: "406 Not Acceptable",  # 服务器无法根据客户端请求的内容特性完成请求
        407: "407 Proxy Authentication Required",  # 请求要求代理的身份认证，与401类似，但请求者应当使用代理进行授权
        408: "408 Request Time-out",  # 服务器等待客户端发送的请求时间过长，超时
        409: "409 Conflict",  # 服务器完成客户端的 PUT 请求时可能返回此代码，服务器处理请求时发生了冲突
        410: "410 Gone",  # 客户端请求的资源已经不存在。410不同于404，如果资源以前有现在被永久删除了可使用410代码，网站设计人员可通过301代码指定资源的新位置
        411: "411 Length Required",  # 服务器无法处理客户端发送的不带Content-Length的请求信息
        412: "412 Precondition Failed",  # 客户端请求信息的先决条件错误
        413: "413 Request Entity Too Large",   # 由于请求的实体过大，服务器无法处理，因此拒绝请求。为防止客户端的连续请求，服务器可能会关闭连接。
        414: "414 Request-URI Too Large",  # 请求的URI过长（URI通常为网址），服务器无法处理
        415: "415 Unsupported Media Type",  # 服务器无法处理请求附带的媒体格式
        416: "416 Requested range not satisfiable",  # 客户端请求的范围无效
        417: "417 Expectation Failed",  # 服务器无法满足Expect的请求头信息
        # 5** 服务器错误，服务器在处理请求的过程中发生了错误
        500: "500 Internal Server Error",  # 服务器内部错误，无法完成请求
        501: "501 Not Implemented",  # 服务器不支持请求的功能，无法完成请求
        502: "502 Bad Gateway",  # 作为网关或者代理工作的服务器尝试执行请求时，从远程服务器接收到了一个无效的响应
        503: "503 Service Unavailable",  # 由于超载或系统维护，服务器暂时的无法处理客户端的请求。延时的长度可包含在服务器的Retry-After头信息中
        504: "504 Gateway Time-out",  # 充当网关或代理的服务器，未及时从远端服务器获取请求
        505: "505 HTTP Version not supported"  # 服务器不支持请求的HTTP协议的版本，无法完成处理
    }
    content_type = {
        "html": "text/html",
        "text": "text/plain",
        "gif": "image/gif",
        "png": "image/png",
        "jpg": "image/jpeg",
        "pdf": "application/pdf",
        "word": "application/msword",
        "xml": "application/xml",
        "json": "application/json"
    }


class MediaFile(HttpBase):
    def __init__(self, data=None, mold="html"):
        if not isinstance(data, bytes):
            err = "data must be bytes"
            raise Exception(err)
        self.data = data
        self.mold = mold

    def get_http(self):
        if self.data is None:
            pass

    def get_mold(self):
        return self.mold

    def get_data(self):
        return self.data

    def set_data(self, data):
        if not isinstance(data, bytes):
            err = "data must be bytes"
            raise Exception(err)
        self.data = data

    def set_mold(self, mold):
        self.mold = mold


class HttpRequest(HttpBase):
    """
    HttpRequest对象，
    打包environ，获取其中的一些重要参数
    """
    def __init__(self, environ: dict):
        """
        初始化HttpRequest

            print(self.method)
            print(self.remote_addr)
            print(self.content_type)
            print(self.parameter)
            print(self.body)
            print(self.path)

        :param environ: 请求体
        """

        self.environ = environ
        # 请求方法
        self.method = environ.get('REQUEST_METHOD', '').lower()
        # 客户端地址
        self.remote_addr = environ.get('REMOTE_ADDR', '')
        # 请求题数据类型
        self.content_type = environ.get('CONTENT_TYPE', '')
        # 请求地址
        self.path = environ.get('PATH_INFO', '')
        # 请求体长度
        self.content_length = environ.get('CONTENT_LENGTH', 0)
        # 请求体
        self.body = environ['wsgi.input'].read(int(self.content_length if self.content_length != '' else 0)).decode()
        # get请求中url中的请求参数
        self.parameter = {}
        # post请求中的表单
        self.form = {}
        # 该请求是被禁止
        self.prohibit = False

        # cookies
        self.cookies = {}

        # 初始化parameter
        self.__init__parameter()
        # 初始化form表单
        self.__init__form()
        # 去除path中的多余的'/'
        self.__remove_redundant_slashes()
        # 初始化cookies
        self.__init__cookies()

    def __init__parameter(self):
        query_string = unquote(self.environ.get('QUERY_STRING', '').encode().decode("utf-8"))
        if query_string != '':
            for item in query_string.split("&"):
                key_value = item.split("=")
                self.parameter[key_value[0]] = key_value[1]

    def __init__form(self):
        if self.body != '':
            if "form" in self.content_type:
                for item in self.body.split("&"):
                    key_value = item.split("=")
                    self.form[key_value[0]] = key_value[1]
            elif "json" in self.content_type:
                self.form = json.loads(self.body)

    def __remove_redundant_slashes(self):
        if self.path == '/' or self.path == '':
            return
        # 去除多余的斜杠
        self.path = self.path.replace("//", "/")
        # 开头却上斜杠就加上
        if self.path[0] != '/':
            self.path = '/' + self.path
        # 去掉尾部的斜杠
        while self.path[-1] == '/':
            self.path = self.path[0:-1]

    def __init__cookies(self):
        pass


class HttpResponse(HttpBase):
    """
    HttpResponse对象
    打包相应结果
    """
    def __init__(self, data=None, charset: str = 'utf-8', status: int = 200):
        # 相应的数据
        self.data = data
        # 状态码
        self.status = HttpResponse.http_status_code.get(status, "200 OK")
        # 编码格式
        self.charset = charset
        # 请求头
        self.headers = {}
        # cookies
        self.cookies = {}

        # 打包传递过来的data数据，
        # 并设置对应的数据格式
        flag, self.data = parse_data(self.data)
        if flag:
            self.content_type = HttpResponse.content_type['json']
        else:
            self.content_type = HttpResponse.content_type['html']

    def set_content_type(self, t: str):
        """
        设置数据格式
        如果对应的格式找不到或使用默认的 'text/html'
            "html": "text/html",
            "text": "text/plain",
            "gif": "image/gif",
            "png": "image/png",
            "jpg": "image/jpeg",
            "pdf": "application/pdf",
            "word": "application/msword",
            "xml": "application/xml",
            "json": "application/json"
        :param t: "html","text","gif","png","jpg","pdf","word","xml","json"
        :return: None
        """
        self.content_type = HttpResponse.content_type.get(t, "text/html")

    def set_status(self, status: int):
        """
        设置状态码
        如果状态码没有找到会使用"200 OK"
            # 1** 信息，服务器收到请求，需要请求者继续执行操作
            # 2** 成功，操作被成功接收并处理
            # 3** 重定向，需要进一步的操作以完成请求
            # 4** 客户端错误，请求包含语法错误或无法完成请求
            # 5** 服务器错误，服务器在处理请求的过程中发生了错误
        :param status: 1**，2**，3**，4**，5**
        :type status: int
        :return: None
        """
        self.status = HttpResponse.http_status_code.get(status, "200 OK")

    def response_headers(self):
        """
        获取响应体的http头
        :return: [('Content-type','text/html; charset=utf-8'),...]
        """
        response_headers = [("Content-type", self.content_type+"; charset="+self.charset)]
        for name in self.headers:
            response_headers += [(name, self.headers[name])]
        return response_headers

    def response_data(self):
        """
        获取响应体
        :return: bytes
        """
        if isinstance(self.data, bytes):
            return [self.data]
        elif isinstance(self.data, str):
            return [self.data.encode('utf-8')]
        else:
            _, data = parse_data(self.data)
            return [data.encode('utf-8')]


class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def before(self, request: HttpRequest) -> HttpRequest:
        """
        在request对象创建后，业务方法执行前启动
        :param request: 请求体
        :type request: HttpRequest
        :return: request
        """
        return request

    @abc.abstractmethod  # 定义抽象方法，无需实现功能
    def after(self, request: HttpRequest, response: HttpResponse) -> tuple:
        """
        在业务方法执行结束后，将数据打包返回给客户端前执行
        :param request: 请求体
        :type request: HttpRequest
        :param response: 响应体
        :type response: HttpResponse
        :return: request, response
        """
        return request, response


def parse_data(data):
    """
    通过递归来解析数据，将数据解析为json格式的字符串
    返回两个参数，bool为True说明字符串为json格式
    :param data: 待解析的数据
    :return: bool,str
    """

    if isinstance(data, bytes):
        return False, data

    if data is None:
        return False, str(data)
    """
    如果使字符串直接返回
    """
    if isinstance(data, str):
        return False, data

    """
    如果是字典，解析字典的每一个值，将其转换为字符串
    并标记is_dict=True
    再借助json.dumps(data)将字典转换为字符串
    """
    if isinstance(data, dict):
        for key in data.keys():
            _, data[key] = parse_data(data[key])
        # print(data)
        res = json.dumps(data, ensure_ascii=False)
        return True, res

    """
    如果是int和float直接转换
    """
    if isinstance(data, int) or isinstance(data, float):
        res = str(data)
        return False, res

    """
    如果是列表
    解析每一个元素将他们转换为字符串
    在借助join连接所有元素
    """
    if isinstance(data, list):
        for i in range(0, len(data)):
            _, data[i] = parse_data(data[i])
        res = ",".join(data)
        res = '{' + res + "}"
        return True, res

    """
    如果是元组或集合
    解析每一个元素将他们转换为字符串，
    然后放入一个列表中,在借助join连接所有元素
    """
    if isinstance(data, tuple) or isinstance(data, set):
        s = []
        for item in data:
            _, t = parse_data(item)
            s.append(t)
        res = " ".join(s)
        res = '{' + res + "}"
        return True, res

    """
    如果不是基本数据类型
    则认为是类
    通过__dict__获取类的所有成员的字典
    然后便利每一个成员将他们变成字符串
    最后借助json.dumps
    """
    tmap = data.__dict__
    for key in tmap.keys():
        _, tmap[key] = parse_data(tmap[key])
    res = json.dumps(tmap, ensure_ascii=False)
    return True, res
