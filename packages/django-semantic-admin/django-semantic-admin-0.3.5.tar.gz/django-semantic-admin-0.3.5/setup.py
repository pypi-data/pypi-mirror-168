# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantic_admin',
 'semantic_admin.filters',
 'semantic_admin.templatetags',
 'semantic_admin.views',
 'semantic_admin.widgets']

package_data = \
{'': ['*'],
 'semantic_admin': ['static/admin/js/*',
                    'static/admin/js/admin/*',
                    'static/semantic_admin/*',
                    'templates/admin/*',
                    'templates/admin/auth/user/*',
                    'templates/admin/edit_inline/*',
                    'templates/admin/includes/*',
                    'templates/admin/widgets/*',
                    'templates/registration/*',
                    'templates/semantic_ui/forms/widgets/*']}

install_requires = \
['django>=3.2']

setup_kwargs = {
    'name': 'django-semantic-admin',
    'version': '0.3.5',
    'description': 'Django Semantic UI Admin theme',
    'long_description': 'Django Semantic UI admin theme\n------------------------------\n<img src="https://raw.githubusercontent.com/globophobe/django-semantic-admin/master/docs/screenshots/change-list.png" alt="django-semantic-admin"/>\n\nA completely free (MIT) [Semantic UI](https://semantic-ui.com/) admin theme for Django. Actually, this is my 3rd admin theme for Django. The first was forgettable, and the second was with [Pure CSS](https://purecss.io/). Pure CSS was great, but lacked JavaScript components.\n\nSemantic UI looks professional, and has great JavaScript components.\n\nLog in to the demo with username `django` and password `semantic-admin`: https://semantic-admin.com\n\nDocumentation is on [GitHub Pages](https://globophobe.github.io/django-semantic-admin/).\n\nWhy?\n----\n* Looks professional, with a nice sidebar.\n* Responsive design, even [tables can stack](https://semantic-ui.com/collections/table.html#stacking) responsively on mobile.\n* JavaScript datepicker and timepicker components.\n* JavaScript selects, including multiple selections, which integrate well with Django autocomplete fields.\n* Semantic UI has libraries for [React](https://react.semantic-ui.com/) and [Vue](https://semantic-ui-vue.github.io/#/), in addition to jQuery. This means this package can be used to style the admin, and custom views can be added with React or Vue components with the same style.\n\n\nInstall\n-------\n\nInstall from PyPI:\n\n```\npip install django-semantic-admin\n```\n\nAdd to `settings.py` before `django.contrib.admin`:\n\n```python\nINSTALLED_APPS = [\n    "semantic_admin",\n    "django.contrib.admin",\n    ...\n]\n```\n\nUsage\n-----\n\nInstead of `admin.ModelAdmin`, `admin.StackedInline`, or `admin.TabularInline`:\n\n```python\nclass ExampleStackedInline(admin.StackedInline):\n    pass\n\nclass ExampleTabularInline(admin.TabularInline):\n    pass\n\nclass ExampleAdmin(admin.ModelAdmin):\n    inlines = (ExampleStackedInline, ExampleTabularInline)\n```\n\nInherit from their `Semantic` equivalents:\n\n```python\nfrom semantic_admin import SemanticModelAdmin, SemanticStackedInline, SemanticTabularInline\n\nclass ExampleStackedInline(SemanticStackedInline):\n    pass\n\nclass ExampleTabularInline(SemanticTabularInline):\n    pass\n\nclass ExampleAdmin(SemanticModelAdmin):\n    inlines = (ExampleStackedInline, ExampleTabularInline)\n```\n\nAwesome optional features\n-------------------------\n\n1. Optional integration with [django_filter](https://github.com/carltongibson/django-filter):\n\n<img src="https://raw.githubusercontent.com/globophobe/django-semantic-admin/master/docs/screenshots/django-filter.png" width="335" alt="django-filter" />\n\nTo enable this awesome feature, add `filterset_class` to your Django admin:\n\n```python\nfrom semantic_admin.filters import SemanticFilterSet\n\nclass DemoFilter(SemanticFilterSet):\n    class Meta:\n        model = Demo\n        fields = ("demo_field",)\n\nclass DemoAdmin(SemanticModelAdmin):\n    filterset_class = DemoFilter\n```\n\n2. HTML preview in Django `autocomplete_fields`:\n\n<img src="https://raw.githubusercontent.com/globophobe/django-semantic-admin/master/docs/screenshots/html5-autocomplete.png" width="670" alt="html5-autocomplete" />\n\nTo enable this awesome feature, add the `semantic_autocomplete` property to your Django model:\n\n```python\nclass DemoModel(models.Model):\n    @property\n    def semantic_autocomplete(self):\n        html = self.get_img()\n        return format_html(html)\n```\n\nContributing\n------------\n\nInstall dependencies with `poetry install`. The demo is built with [invoke tasks](https://github.com/globophobe/django-semantic-admin/blob/master/demo/tasks.py). For example, `cd demo; invoke build`.\n\n\nNotes\n-----\nPlease note, this package uses [Fomantic UI](https://fomantic-ui.com/) the official community fork of Semantic UI.\n',
    'author': 'Alex',
    'author_email': 'globophobe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/globophobe/django-semantic-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
