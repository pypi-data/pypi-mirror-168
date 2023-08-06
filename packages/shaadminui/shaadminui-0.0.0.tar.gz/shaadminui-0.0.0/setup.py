# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shaadminui', 'shaadminui.migrations', 'shaadminui.templatetags']

package_data = \
{'': ['*'],
 'shaadminui': ['locale/zh-Hans/LC_MESSAGES/*',
                'locale/zh/LC_MESSAGES/*',
                'static/admin/components/Ionicons/css/*',
                'static/admin/components/Ionicons/fonts/*',
                'static/admin/components/bootstrap-colorpicker/dist/css/*',
                'static/admin/components/bootstrap-colorpicker/dist/img/bootstrap-colorpicker/*',
                'static/admin/components/bootstrap-colorpicker/dist/js/*',
                'static/admin/components/bootstrap-datepicker/dist/css/*',
                'static/admin/components/bootstrap-datepicker/dist/js/*',
                'static/admin/components/bootstrap-datepicker/dist/locales/*',
                'static/admin/components/bootstrap-daterangepicker/*',
                'static/admin/components/bootstrap/dist/css/*',
                'static/admin/components/bootstrap/dist/fonts/*',
                'static/admin/components/bootstrap/dist/js/*',
                'static/admin/components/datatables.net-bs/*',
                'static/admin/components/datatables.net-bs/css/*',
                'static/admin/components/datatables.net-bs/js/*',
                'static/admin/components/datatables.net/*',
                'static/admin/components/datatables.net/js/*',
                'static/admin/components/fastclick/lib/*',
                'static/admin/components/font-awesome/css/*',
                'static/admin/components/font-awesome/fonts/*',
                'static/admin/components/jquery-slimscroll/*',
                'static/admin/components/jquery/dist/*',
                'static/admin/components/jquery/external/sizzle/*',
                'static/admin/components/jquery/external/sizzle/dist/*',
                'static/admin/components/select2/dist/css/*',
                'static/admin/components/select2/dist/js/*',
                'static/admin/components/select2/dist/js/i18n/*',
                'static/admin/dist/css/*',
                'static/admin/dist/css/alt/*',
                'static/admin/dist/css/skins/*',
                'static/admin/dist/img/*',
                'static/admin/dist/js/*',
                'static/admin/dist/js/pages/*',
                'static/admin/plugins/bootstrap-slider/*',
                'static/admin/plugins/bootstrap-wysihtml5/*',
                'static/admin/plugins/iCheck/*',
                'static/admin/plugins/iCheck/flat/*',
                'static/admin/plugins/iCheck/futurico/*',
                'static/admin/plugins/iCheck/line/*',
                'static/admin/plugins/iCheck/minimal/*',
                'static/admin/plugins/iCheck/polaris/*',
                'static/admin/plugins/iCheck/square/*',
                'static/admin/plugins/input-mask/*',
                'static/admin/plugins/input-mask/phone-codes/*',
                'static/admin/plugins/jQueryUI/*',
                'static/admin/plugins/jvectormap/*',
                'static/admin/plugins/pace/*',
                'static/admin/plugins/seiyria-bootstrap-slider/*',
                'static/admin/plugins/seiyria-bootstrap-slider/css/*',
                'static/admin/plugins/timepicker/*',
                'templates/admin/*',
                'templates/admin/auth/user/*',
                'templates/admin/edit_inline/*',
                'templates/admin/includes/*',
                'templates/adminlte/*',
                'templates/adminlte/widgets/*',
                'templates/registration/*']}

install_requires = \
['importlib_metadata>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'shaadminui',
    'version': '0.0.0',
    'description': '这是一个django 后端主题，基于adminlte修改的。',
    'long_description': '# shaAdminUI\n\n\n[![PyPI version](https://badge.fury.io/py/shaadminui.svg)](https://badge.fury.io/py/shaadminui)\n![versions](https://img.shields.io/pypi/pyversions/shaadminui.svg)\n[![GitHub license](https://img.shields.io/github/license/mgancita/shaadminui.svg)](https://github.com/mgancita/shaadminui/blob/main/LICENSE)\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n这是一个django 后端主题，基于adminlte修改的。\n\n\n- 开源许可: MIT\n- 文档: https://llango.github.io/shaadminui.\n\n\n## 特征\n\n* TODO\n\n## 制作\n\n\n该包使用 [Cookiecutter](https://github.com/audreyr/cookiecutter) 和 [`llango/cookiecutter-mkdoc-shapackage`](https://github.com/llango/cookiecutter-mkdoc-shapackage/) 项目模版创建。\n',
    'author': 'Rontomai',
    'author_email': 'rontomai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/llango/shaadminui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
