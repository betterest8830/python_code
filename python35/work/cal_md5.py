# coding=utf8


import hashlib
g_zip_password = b'sogounovel'
mpw = hashlib.md5()
mpw.update(g_zip_password)
zip_password = mpw.hexdigest()
print(zip_password)