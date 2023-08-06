from rdflib import URIRef, Graph
from rdflib.namespace import NamespaceManager
from rdflib.term import Node, Variable
from rdflib.plugins.sparql.parser import ConstructTriples
from rdflib.plugins.sparql.parserutils import CompValue
from rdfhelpers.rdfhelpers import expandQName

def parseConstructTriples(template):
    # This is ugly, and perhaps there is a more sane way of doing this, but for now, parsing the
    # SPARQL CONSTRUCT clause triple patterns results in a list the single element of which is an
    # object (a ParamValue) that has a list of tokens (unresolved RDF terms).
    return ConstructTriples.parseString(template)[0].tokenList

class Constructor:
    ns_mgr = NamespaceManager(Graph())

    def __init__(self, template, ns_mgr=None):
        self.template = self.parseTemplate(template)
        self.ns_mgr = ns_mgr or self.__class__.ns_mgr

    @classmethod
    def bind(cls, prefix, namespace, override=True, replace=False):
        cls.ns_mgr.bind(prefix, namespace, override=override, replace=replace)

    @classmethod
    def resolveTerm(cls, item, ns_mgr=None):
        if isinstance(item, Node):
            return item
        elif isinstance(item, CompValue):
            if item.name == "pname":
                return URIRef(expandQName(item['prefix'], item['localname'], ns_mgr or cls.ns_mgr))
            elif item.name == "literal":
                return item['string']
        raise ValueError("Unrecognized token {}".format(str(item)))

    @classmethod
    def parseTemplate(cls, template, ns_mgr=None):
        tokens = [cls.resolveTerm(t, ns_mgr=ns_mgr) for t in parseConstructTriples(template)]
        return [tuple(tokens[i:i + 3]) for i in range(0, len(tokens), 3)]

    @classmethod
    def expandTerm(cls, term, bindings: dict):
        value = bindings.get(str(term), None) if isinstance(term, Variable) else term
        if value is None:
            return []
        elif isinstance(value, list):
            return value
        else:
            return [value]

    @classmethod
    def expandTemplate(cls, template, bindings: dict):
        for s, p, o in template:
            for ss in cls.expandTerm(s, bindings):
                for pp in cls.expandTerm(p, bindings):
                    for oo in cls.expandTerm(o, bindings):
                        yield ss, pp, oo

    @classmethod
    def parseAndExpand(cls, template, bindings: dict, ns_mgr=None):
        return cls.expandTemplate(cls.parseTemplate(template, ns_mgr=ns_mgr), bindings)

    def expand(self, **bindings):
        return self.expandTemplate(self.template, bindings)
