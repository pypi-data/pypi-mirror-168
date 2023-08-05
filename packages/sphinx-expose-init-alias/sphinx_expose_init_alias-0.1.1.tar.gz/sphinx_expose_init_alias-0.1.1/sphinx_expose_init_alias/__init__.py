import sphinx.application as sphinx_app


from sphinx_expose_init_alias.documenter import AliasDocumenter
from sphinx_expose_init_alias.documenter import AliasModuleDocumenter
from sphinx_expose_init_alias.documenter import AliasClassDocumenter
from sphinx_expose_init_alias.documenter import AliasFunctionDocumenter
from sphinx_expose_init_alias.documenter import AliasExceptionDocumenter
from sphinx_expose_init_alias.callback import maybe_skip_member
from sphinx_expose_init_alias.exception import SEIAValueError
from sphinx_expose_init_alias.__about__ import __version__


def setup(app: sphinx_app):
    app.setup_extension('sphinx.ext.autodoc')  # Require autodoc extension
    app.add_autodocumenter(AliasDocumenter)
    app.add_autodocumenter(AliasModuleDocumenter)
    app.add_autodocumenter(AliasClassDocumenter)
    app.add_autodocumenter(AliasFunctionDocumenter)
    app.add_autodocumenter(AliasExceptionDocumenter)
    app.connect('autodoc-skip-member', maybe_skip_member)
    return {
        "version": __version__
    }