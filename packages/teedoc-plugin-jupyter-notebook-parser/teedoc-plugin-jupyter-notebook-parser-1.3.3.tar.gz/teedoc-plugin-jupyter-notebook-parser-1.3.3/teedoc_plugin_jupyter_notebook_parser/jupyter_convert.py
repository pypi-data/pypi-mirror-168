

from nbconvert.exporters.templateexporter import TemplateExporter
from nbconvert import HTMLExporter
import nbformat
import re
import os
import yaml

curr_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(curr_dir, "templates")

TemplateExporter.extra_template_basedirs=[templates_dir]
html_exporter = HTMLExporter()
html_exporter.template_name = "lab"
html_exporter.template_file = 'base.html.j2'
html_exporter.anchor_link_text = " " # set anchor_link empty

def convert_ipynb_to_html_body(path):
    global html_exporter
    with open(path, encoding="utf-8") as f:
        content = nbformat.read(f, as_version=4)
        body, resources = html_exporter.from_notebook_node(content)
        return body

class HTML:
    def __init__(self):
        self.title = ""
        self.desc = ""
        self.keywords = []
        self.tags = []
        self.body = ""
        self.toc = ""
        self.metadata = []
        self.raw = ""

def parse_metadata(cell):
    '''
        @cell {'cell_type': 'markdown',
                'metadata': {'id': 'rX8mhOLljYeM'},
                'source': '---\ntitle: 部署 teedoc 生成的网站\nkeywords: teedoc, 部署\ndesc: teedoc 生成的网站部署到服务器\n---'
              }
    '''
    content = cell["source"].strip()
    meta = {
        "title": "",
        "keywords": "",
        "desc": "",
        "tags": "",
        "id": "",
        "class": ""
    }
    have_metadata = False
    if not content:
        return have_metadata, meta, ""
    if not content.startswith("---"):
        content_list = content.split("\n")
        if content_list[0].startswith("# "): # h1 header
            meta["title"] = content_list[0][2:]
            cell_content = "\n".join(content_list[1:])
            have_metadata = True
        elif len(content_list) > 1 and content_list[1].startswith("==="): # h1 header
            meta["title"] = content_list[0]
            cell_content = "\n".join(content_list[2:])
            have_metadata = True
        else:
            cell_content = content
        return have_metadata, meta, cell_content
    items_all = re.findall("[-]{2}[-]$\n(.*?)\n[-]{3}(.*)", content, re.MULTILINE|re.DOTALL)
    if len(items_all) > 0:
        meta = yaml.load(items_all[0][0].strip(), Loader=yaml.Loader)
        cell_content = items_all[0][1].strip()
        have_metadata = True
    return have_metadata, meta, cell_content

def get_search_content(cells):
    content = ""
    for cell in cells:
        if cell["cell_type"] == "markdown":
            for item in cell["source"]:
                content += item.strip()
        elif cell["cell_type"] == "code":
            for item in cell["source"]:
                content += item.strip()
            for item in cell["outputs"]:
                if "text" in item:
                    content += item["text"].strip()
                if "text/plain" in item:
                    content += item["text/plain"].strip()
    return content


def convert_ipynb_to_html(path):
    global html_exporter
    html = HTML()
    with open(path, encoding="utf-8") as f:
        content = nbformat.read(f, as_version=4)
        have_meta, html.metadata, first_cell_content = parse_metadata(content.cells[0])
        if have_meta:
            if first_cell_content:
                content.cells[0]["source"] = first_cell_content
            else:
                content.cells = content.cells[1:]
        elif first_cell_content:
            content.cells[0]["source"] = first_cell_content
        html.title = html.metadata.get("title", "")
        html.keywords = (html.metadata["keywords"] if type(html.metadata["keywords"]) == list else html.metadata["keywords"].split(",")) if html.metadata.get("keywords") else []
        html.desc = html.metadata.get("desc", "")
        html.tags = (html.metadata["tags"] if type(html.metadata["tags"]) == list else html.metadata["tags"].split(",")) if html.metadata.get("tags") else []
        body, resources = html_exporter.from_notebook_node(content)
        html.raw = get_search_content(content.cells)
        html.body = body
    return html

if __name__ == "__main__":
    import sys
    notebook = "e:/main/projects/teedoc/examples/local_test/docs/get_started/zh/syntax/syntax_notebook.ipynb"
    # notebook = sys.argv[1]
    TemplateExporter.extra_template_basedirs=[templates_dir]
    html_exporter = HTMLExporter()
    # print(html_exporter.template_name)
    html_exporter.template_name = 'lab'
    html_exporter.template_file = "base.html.j2"
    print(TemplateExporter.extra_template_basedirs)

    with open(notebook, encoding="utf-8") as f:
        content = nbformat.read(f, as_version=4)
        body, resources = html_exporter.from_notebook_node(content)
        # from html_toc import HtmlTocParser
        # parser = HtmlTocParser()
        # parser.feed(body)
        # print(parser.toc())
        # html = parser.toc_html(depth=2, lowest_level=5)
        # print(html)
        print(body)
        # print(type(resources))
        # print("Resources:", resources.keys())
        # print("Metadata:", resources['metadata'].keys())
        # print("Inlining:", resources['inlining'].keys())
        # print("Extension:", resources['output_extension'])
        # print(len(resources['inlining']["css"]))
        # with open("out/a.css", "w") as f:
        #     f.write(resources['inlining']["css"][1])
