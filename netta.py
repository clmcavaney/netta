
#!/usr/bin/env python3 
"""
Netta. An application for managing, transforming, packaging and publishing data.

"""
import converters
import os
import json
from PIL import Image

from flask import Flask
from flask import escape
from flask import render_template, send_from_directory, request

app = Flask(__name__)
import os
import subprocess
from os.path import expanduser
import converters
from package import Package

converter_stash=converters.Converters("converters")

home = expanduser("~")

package = Package("./package.json")

@app.route("/js/<path:p>")
def js(p):
     return send_from_directory("./js", p)

@app.route('/')
def home_page():
    return render_template("dir.html", out = "<a href='/explore/'>Explore</a>")

@app.route('/save/package',methods=['GET', 'POST'])
def save_package():
    content = request.get_json(force=True)
    package.save(content)
    return "yep"

@app.route('/get/package')
def get_package():
    return package.read()

@app.route('/package/zip')
def zip_package():
    package.zipped_bag(os.path.join(home,"package"))
    return("OK")

@app.route('/explore/', defaults={'p':''})
@app.route('/explore/<path:p>')
def dir_list(p):
    list_this = os.path.join(home, p)
    heading = "<h1>%s <a href='..'>..</a></h1>" % list_this
    out = ""
    files = "<table width='100%'>"
    dirs = "<ul>"
    # TODO - make a class for directories and files
    for filename in os.listdir(list_this):
        if filename.startswith("."):
            continue
        full_path = os.path.join(list_this, filename)
        if os.path.isdir(full_path):
            if filename not in ['_renditions_']:
                dirs += "<li><a href='./{de}/'>{d}</a></li>".format(d=filename,de=escape(filename))
        else:
            _, ext = os.path.splitext(filename)
            converter = converter_stash.get_by_ext(ext)
            conv = converter(full_path)

            
            file_meta = conv.get_metadata()
            
            meta = "<details class='show-meta' data-placement='top'><table>"
            for key, value in file_meta.items():
                meta += "<tr><td>{key}</td><td>{value}</td></tr>".format(key=escape(key), value=escape(value))
            meta += "</table></details>"
            title = conv.get_metadata_item('dc:title')
            if not title or isinstance(title, list):
                title = filename

            viewable = conv.get_viewable()
            if viewable:
                viewable_path, viewable_mime = viewable
                file =  "<span class='view' href='{full_path}' data-mime='{m}' title='{f}'>{t}</span>".format(full_path=escape(full_path), f=escape(filename),
                                                                                                                   t=escape(title), m = viewable_mime)
            else:
                file =  escape(title)
            
            thumb = "<img src='/thumbs{full_path}' width='128'>".format(full_path=full_path) if conv.has_thumbnail_method() else ""
                 
            files += "<tr><td><h1 class='ADD'>+</h1></td><td>{file}</td><td>{thumb}</td><td>{meta}</td></tr>".format(
                      file=file,meta=meta,thumb=thumb)
            
    files += "</table>"
    dirs += "</ul>"
    
    
    return (render_template('dir.html', files = files, dirs= dirs, heading=heading, full_path=list_this))



@app.route('/thumbs/<path:path>')
# Show thumbnails
def tumbs(path):
    path = "/" + path
    _, ext  = os.path.splitext(path)
    conv = converter_stash.get_by_ext(ext)
    if conv:
        converter = conv(path)
        if converter.has_thumbnail_method():
            converter.make_thumbnail()
            return send_from_directory(converter.renditions_store.thumb_dir , converter.renditions_store.thumb_filename, mimetype='image/png')
   
    


    
@app.route('/view/<path:path>')
# Show thumbnails
def view(path):
    path = "/" + path
    _, ext  = os.path.splitext(path)
    conv = converter_stash.get_by_ext(ext)
    if conv:
        converter = conv(path)
        if converter.has_pdf_method():
            path = converter.renditions_store.pdf_path
    dir, filename = os.path.split(path)
    return send_from_directory(dir, filename)



@app.route('/wrap/<path:path>')

def wrap(path):
    # TODO: Remove repetition here
    path = "/" + path
    _, ext  = os.path.splitext(path)
    mime = ""
    conv = converter_stash.get_by_ext(ext)
    if conv:
        converter = conv(path)
        if converter.has_pdf_method():
            mime = "type='application/pdf'"
    out = '<embed src="/view{path}" {mime}></embed>'.format(path=path, mime=mime)
    return (render_template('wrap.html', out=out, path=path))

if __name__ == '__main__':
    app.debug = True
    app.run()
