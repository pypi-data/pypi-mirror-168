# MyHttp v1.1.4

## 1. Usage / 使用方式

(1) http(url:str,Method:str="GET",Header:dict={},Timeout:int=None,ToJson:bool=True,Body:str="",Decode:bool=True,Retry:bool=True,ForceHttps:bool=False)

    url: need to begin with 'http://' or 'https://' / 需要带有 'http://' 或 'https://'
    Timeout: unit ms, default value is 2000ms. You can also set default timeout with setDefaultTimeout() / 单位为毫秒，默认为2000毫秒。可以通过setDefaultTimeout()修改默认值。
    Retry: If timeout occurs in the first time, the program will retry with the timeout of three times of the original value. You can disable this retry by setting Retry to False.
            如果第一次连接超时, 程序会自动尝试重新连接, timeout 是第一次的3倍。如果 Retry 为 False, 程序不会重新连接。
    
    Return value: dict, it has five keys: status, code, header, text, extra
    返回值为 dict, 其中有 5 个 key: status, code, header, text, extra
    
    Status:
    -1: 无网络 / No Internet Connection
    -2: 超时 / Timeout
    -3: 域名不存在 / Domian not exists
    -4: 其它问题, 主要是代理服务器设置错误 / Other problem, mainly proxy server error
    -5: 对方网站不支持 https, 但强制要求 https 链接 / The website does not support https, but you force https connection.
    1: 不是 UTF-8 编码, text 返回空字符串 / Not UTF-8 encode, the return value of text will be empty str
    2: 不是 Json 格式(在 toJSON=True 的前提下) / Not in Json format (when toJSON=True)
    3: 对方网站不支持https, 但是却使用了https连接, 这种情况会自动切换为http连接, 若此次status不为0, 返回该status, 若为0, 返回3
    The website does not support https. It will change to http automatically in this situation. If the status this time is 0, the status will be 3. If not 0, it will return this status.
    
    code: Http status code / Http 状态码
    
    header: response header
    
    text: response body
    
    extra: when status is 1, the binary text will be stored in extra; when status is 2, the original text will be stored in extra. In other cases, it will be ''
    status 为 1 时, 会将二进制信息储存在 extra 中, status 为 2 时, 会将原始字符串储存在 extra 中, 其它情况为空字符串。

(2) testInternet()
    
    Return 0 when there is Internet connection; return -1 when there is no Internet connection.
    如果有网络连接, 返回 0; 如果没有网络连接, 返回 -1
    
    Default testing url is 'https://apple.com' / 默认测试链接为 'https://apple.com'
    You can change default testing url through setDefaultTestingUrl() / 可通过 setDefaultTestingUrl() 修改默认测试链接
    
## 2. Install / 安装
    
    pip3 install myHttp

## 3. Other notification / 其它说明

    Emial / 邮箱: jtc1246@outlook.com
    License: GPL v2
    Requirement / 要求: Python 3
