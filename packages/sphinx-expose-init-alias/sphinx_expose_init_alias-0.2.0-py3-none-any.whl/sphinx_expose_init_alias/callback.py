import sphinx.application as sphinx_app
import docutils.nodes as doc_n
import sphinx.ext.autodoc.typehints as sphinx_ath


def maybe_skip_member(app, what, name, obj, skip, options):
    if what == 'aliasmodule':
        return False


def merge_typehints(app: sphinx_app.Sphinx, domain: str, objtype: str, contentnode: doc_n.Element) -> None:
    if not app.config.sphinx_expose_init_alias_show_description:
        if len(contentnode.children) == 2:
            child = contentnode.children[0]
            if child.astext().startswith('alias of'):
                contentnode.children.pop(1)
                return
    return sphinx_ath.merge_typehints(app, domain, objtype, contentnode)


