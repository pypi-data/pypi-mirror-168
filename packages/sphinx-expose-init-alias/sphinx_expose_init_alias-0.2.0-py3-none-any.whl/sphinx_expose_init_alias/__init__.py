import sphinx.application as sphinx_app


from sphinx_expose_init_alias.documenter import AliasDocumenter
from sphinx_expose_init_alias.documenter import AliasModuleDocumenter
from sphinx_expose_init_alias.documenter import AliasClassDocumenter
from sphinx_expose_init_alias.documenter import AliasFunctionDocumenter
from sphinx_expose_init_alias.documenter import AliasExceptionDocumenter
from sphinx_expose_init_alias.callback import maybe_skip_member
from sphinx_expose_init_alias.callback import merge_typehints
from sphinx_expose_init_alias.exception import SEIAValueError
from sphinx_expose_init_alias.__about__ import __version__


AliasD = AliasDocumenter
AliasMD = AliasModuleDocumenter
AliasCD = AliasClassDocumenter
AliasFD = AliasFunctionDocumenter
AliasED = AliasExceptionDocumenter


def setup(app: sphinx_app.Sphinx):
    app.setup_extension('sphinx.ext.autodoc')  # Require autodoc extension
    app.add_config_value("sphinx_expose_init_alias_as_attr", False, True)
    app.add_config_value("sphinx_expose_init_alias_show_description", False, True)
    app.add_config_value("sphinx_expose_init_alias_with_not_alias", False, True)
    app.add_autodocumenter(AliasDocumenter)
    app.add_autodocumenter(AliasModuleDocumenter)
    app.add_autodocumenter(AliasClassDocumenter)
    app.add_autodocumenter(AliasFunctionDocumenter)
    app.add_autodocumenter(AliasExceptionDocumenter)
    app.connect('autodoc-skip-member', maybe_skip_member)
    app.connect('object-description-transform', merge_typehints)
    return {
        "version": __version__
    }
