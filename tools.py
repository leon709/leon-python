import sys, json
import flask
from flask import make_response, render_template
import traceback

app = flask.Flask(__name__)
app.jinja_loader.searchpath.append("/home/leon/mycodebase/leon-python")


import logging
logger = logging.getLogger("tools")

@app.route("/")
def hello():
    print app.jinja_loader.searchpath
    
    return "Welcome!"

@app.route("/test/<page>")
def test(page):
    
    return render_template(page + ".html")
    
if __name__ == "__main__":
    import os, time
    mt = os.stat(sys.argv[0]).st_mtime
    logger.info("Code update time: %s", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(mt)))
    
    app.run(debug=True, host='0.0.0.0')
    logger.info("Webtool started...")