#! /usr/bin/env python
import os
import json

# Change to script folder
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# wheezy templating engine
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

NOTEBOOKS_OUTPUT = os.path.join(dname, '..','content', 'pages', 'notebooks.md')



templateEngine = Engine(
    loader=FileLoader( [dname] ),
    extensions=[CoreExtension()]
)

 
def generate_markdown(option_dict, template_file, output ):

    with open(output,'wt') as outfile:
        template = templateEngine.get_template(template_file)
        outfile.write( template.render( option_dict ) )

# Get all notebook files in the notebooks folder (repo)
notebook_files = []
notebook_dir = os.path.join(dname, 'notebooks')

for cur, dirs, files in os.walk(notebook_dir, topdown=True, onerror=None, followlinks=False):
    notebook_files.extend( [os.path.join(cur, f) for f in files if f.endswith('.ipynb') ] )

# We now have a list of all notebook paths
notebooks = []    
for nbf in notebook_files:
    with open(nbf, 'r') as f:
        nb = json.loads(f.read(-1))
        metadata = nb["metadata"]
        metadata['notebook_path'] = nbf
        metadata['examples'] = { x:nbf.replace('.ipynb',x) for x in ['.html','.pdf'] if os.path.isfile(nbf.replace('.ipynb',x))}

        if metadata['name'] == '':
            metadata['name'] = os.path.basename(nbf)

        if 'description' not in metadata:
            metadata['description'] = ''

        notebooks.append( metadata )

generate_markdown( {'notebooks':notebooks}, 'notebook-list.md', NOTEBOOKS_OUTPUT )
    

