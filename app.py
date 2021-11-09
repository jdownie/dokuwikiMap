#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import os, sys, json, random, html, tempfile, graphviz
from flask import Flask, render_template, send_file, request, current_app

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# ### The user interface...

@app.route('/favicon.ico')
def favicon():
  return current_app.send_static_file("favicon.ico")

@app.route('/js/<page>')
@app.route('/css/<page>')
@app.route('/cfg/<page>')
def cssFile(page):
  return current_app.send_static_file(page)

@app.route('/')
@app.route('/<page>')
def ui(page = None):
  page = "index.html" if page == None else page
  if page in [ "wiki.json", "menu.json" ]:
    ret = current_app.send_static_file(page)
  else:
    ret = render_template(page)
  return ret

@app.route('/<node>.svg')
def graph(node):
  node = node.replace(".", "/")
  fin = open("static/wiki.json", "r")
  wiki = json.load(fin)
  fin.close()
  fin = open("static/menu.json", "r")
  menu = json.load(fin)
  fin.close()
  dot = graphviz.Digraph(format="svg", engine="dot")
  nodes = list()
  edges = list()
  nodes.append(node)
  for src, dsts in wiki.items():
    if src == node:
      for dst in dsts:
        if not dst in menu:
          edges.append([ src, dst ])
          if not dst in nodes:
            nodes.append(dst)
    if node in dsts and not node in menu:
      edges.append([ src, node ])
      if not src in nodes:
        nodes.append(src)
  for n in nodes:
    dot.node(n)
  for e in edges:
    dot.edge(e[0], e[1], constraint="true")
  fout = open("/tmp/debug", "w")
  fout.write(json.dumps(nodes))
  fout.write(json.dumps(edges))
  fout.close()
  fout = tempfile.NamedTemporaryFile(delete=False)
  tmp = fout.name
  fout.write(dot.pipe())
  fout.close()
  fname = "root" if node == "/" else node
  ret = send_file(tmp, as_attachment=True, attachment_filename="{0}.svg".format(fname))
  os.remove(tmp)
  return ret

