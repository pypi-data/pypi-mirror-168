
from flask import Flask

app = Flask(__name__)

"""
使用方法如下：
    >> 该方法用来制作接口给后端数据

    from negentropior.tools.Web.flaskAPI import app

    @app.route('/index': 页面地址, method = ['post'])
    def give_data():
        ...

    app.run(host=..., port=..., *args, **kwargs)
"""