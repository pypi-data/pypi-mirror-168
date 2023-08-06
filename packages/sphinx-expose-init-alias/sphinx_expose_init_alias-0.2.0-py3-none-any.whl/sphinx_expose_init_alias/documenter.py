from typing import Tuple, Any, Optional

import docutils.statemachine as doc_sm
import sphinx.ext.autodoc as autodoc
import sphinx.locale as sphinx_i18n

from .exception import SEIAValueError


class AliasMember:
    def __init__(self, member, has_type=False):
        self._member = member
        self.has_type = has_type

    @property
    def member(self):
        return self._member


def wrap_member(obj_member: autodoc.ObjectMember, has_type=True):
    return autodoc.ObjectMember(obj_member[0], AliasMember(obj_member[1], has_type), *obj_member[2:])


class AliasModuleDocumenter(autodoc.ModuleDocumenter):
    objtype = 'aliasmodule'
    directivetype = autodoc.ModuleDocumenter.objtype
    priority = 10 + autodoc.ModuleDocumenter.priority
    option_spec = dict(autodoc.ModuleDocumenter.option_spec)

    def import_object(self, raiseerror: bool = False) -> bool:
        ret = super().import_object(raiseerror)
        if not ret:
            return ret
        if type(self.object).__name__ != "module":
            if raiseerror:
                raise SEIAValueError(sphinx_i18n.__("aliasmodule '%s' should be package") % self.fullname)
            else:
                autodoc.logger.warning(sphinx_i18n.__("aliasmoudle '%s' should be package") % self.fullname, type='autodoc')
                return False
        if self.object.__file__.endswith('/__init__.py'):
            return True
        if raiseerror:
            raise SEIAValueError(sphinx_i18n.__("aliasmodule '%s' should be package") % self.fullname)
        else:
            autodoc.logger.warning(sphinx_i18n.__("aliasmoudle '%s' should be package") % self.fullname, type='autodoc')
        return False

    def get_object_members(self, want_all: bool) -> Tuple[bool, autodoc.ObjectMembers]:
        _, members = super().get_object_members(want_all)
        prefix = f"{self.object.__name__}."
        ret = []
        has_type = not self.config.sphinx_expose_init_alias_as_attr
        with_not_alias = self.config.sphinx_expose_init_alias_with_not_alias
        for member in members:
            if not hasattr(member[1], "__module__"):
                if with_not_alias:
                    ret.append(member)
                continue
            if not member[1].__module__.startswith(prefix):
                if with_not_alias:
                    ret.append(member)
                continue
            if member.skipped:
                continue
            ret.append(wrap_member(member, has_type))
        return False, ret


class AliasDocumenter(autodoc.ModuleLevelDocumenter):
    objtype = 'alias'
    directivetype = autodoc.AttributeDocumenter.objtype
    priority = 100000000

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return isinstance(member, AliasMember)

    def get_object_members(self, want_all: bool) -> Tuple[bool, autodoc.ObjectMembers]:
        return False, []

    def format_signature(self, **kwargs: Any) -> str:
        if self.config.sphinx_expose_init_alias_as_attr:
            return ''
        return super().format_signature(**kwargs)

    def add_content(self, more_content: Optional[doc_sm.StringList]) -> None:
        if self.config.autodoc_typehints_format == "short":
            alias = autodoc.restify(self.object, "smart")
        else:
            alias = autodoc.restify(self.object)
        more_content = doc_sm.StringList([sphinx_i18n._('alias of %s') % alias], source='')
        for line, src in zip(more_content.data, more_content.items):
            self.add_line(line, src[0], src[1])


class AliasFunctionDocumenter(AliasDocumenter):
    objtype = 'aliasfunction'
    directivetype = autodoc.FunctionDocumenter.objtype
    priority = AliasDocumenter.priority + 2

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        if not AliasDocumenter.can_document_member(member, membername, isattr, parent):
            return False
        if not member.has_type:
            return False
        ret = autodoc.FunctionDocumenter.can_document_member(member.member, membername, isattr, parent)
        autodoc.logger.debug("%s, %s, is function: %s", membername, member.member, ret)
        return ret


class AliasClassDocumenter(AliasDocumenter):
    objtype = 'aliasclass'
    directivetype = autodoc.ClassDocumenter.objtype
    priority = AliasDocumenter.priority + 1

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        if not AliasDocumenter.can_document_member(member, membername, isattr, parent):
            return False
        if not member.has_type:
            return False
        ret = autodoc.ClassDocumenter.can_document_member(member.member, membername, isattr, parent)
        autodoc.logger.debug("%s, %s, is class: %s", membername, member.member, ret)
        return ret


class AliasExceptionDocumenter(AliasDocumenter):
    objtype = 'aliasexception'
    directivetype = autodoc.ExceptionDocumenter.objtype
    priority = AliasDocumenter.priority + 10

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        if not AliasDocumenter.can_document_member(member, membername, isattr, parent):
            return False
        if not member.has_type:
            return False
        ret = autodoc.ExceptionDocumenter.can_document_member(member.member, membername, isattr, parent)
        autodoc.logger.debug("%s, %s, is exception: %s", membername, member.member, ret)
        return ret
