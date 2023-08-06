from urllib import parse
import hashlib

# 合并相对URL，并且处理掉 ../ 类似的地址
def process_url(referer, url):
    url = parse.urljoin(referer, url)
    u = parse.urlparse(url)
    _u = parse.urlparse(parse.urljoin(f'{u.scheme}://{u.netloc}', u.path))
    return parse.ParseResult(u.scheme, u.netloc, _u.path, u.params, u.query, u.fragment).geturl()


def get_hash(data_str):
    return hashlib.md5(data_str.encode('utf8')).hexdigest()
