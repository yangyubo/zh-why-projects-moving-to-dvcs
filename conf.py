# -*- coding: utf-8 -*-



import sys, os
project = u'为什么软件项目从集中式迁移到分布式版本控制系统的热情持续不减?'
copyright = u''
version = u''
release = u''

source_suffix = '.rst'
master_doc = 'index'
language = 'zh_CN'
exclude_patterns = ['_build']
extensions = ['sphinx.ext.pngmath']
pygments_style = 'sphinx'

html_title = u'为什么软件项目从集中式迁移到分布式版本控制系统的热情持续不减?'
html_theme = 'haiku'
html_theme_path = ['../../../templates/sphinx', ]
htmlhelp_basename = 'why-projects-moving-to-dvcs'
html_add_permalinks = None

file_insertion_enabled = False
latex_documents = [
  ('index', 'why-projects-moving-to-dvcs.tex', u'为什么软件项目从集中式迁移到分布式版本控制系统的热情持续不减?',
   u'', 'manual'),
]

exclude_patterns = ['README.rst']


#Add sponsorship and project information to the template context.
context = {
    'MEDIA_URL': "/media/",
    'slug': 'why-projects-moving-to-dvcs',
    'name': u'为什么软件项目从集中式迁移到分布式版本控制系统的热情持续不减?',
    'analytics_code': '',
}

html_context = context
