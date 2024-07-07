#!/usr/bin/env python3
"""
This module runs the flask app
"""
from .views import create_app

app = create_app('dev')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
