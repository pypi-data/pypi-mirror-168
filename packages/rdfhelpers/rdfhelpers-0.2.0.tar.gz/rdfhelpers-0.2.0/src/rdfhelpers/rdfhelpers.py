from rdflib import URIRef, BNode, Graph, RDF
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdfhelpers.templated import Templated, TemplatedQueryMixin
import re

# GLOSSARY
#
# This code uses certain terms or words in specific meanings:
# - "container" -- a composite object, an instance of any of the subclasses of rdfs:Container.
# - "context" -- something implemented as a named graph in the back-end.

# HELPFUL STUFF

# Make a new Graph instance from triples (an iterable)
def graphFrom(triples, add_to=None, graph_class=Graph):
    g = add_to or graph_class()
    for triple in triples:
        g.add(triple)
    return g if len(g) > 0 else None

def expandQName(prefix, local_name, ns_mgr):
    ns = ns_mgr.store.namespace(prefix)
    if ns is not None:
        return str(ns) + local_name
    else:
        raise KeyError("Namespace prefix {} is not bound".format(prefix))

def URI(u):
    return u if isinstance(u, URIRef) or u is None else URIRef(u)

# Helpful graph accessors

def getvalue(graph, node, predicate):
    return next(graph.objects(node, predicate), None)

def setvalue(graph, node, predicate, value):
    graph.remove((node, predicate, None))
    if value is not None:
        graph.add((node, predicate, value))

def addvalues(graph, node, predicates_and_values: dict):
    for predicate, value in predicates_and_values.items():
        graph.add((node, predicate, value))

def setvalues(graph, node, predicates_and_values: dict):
    for predicate, value in predicates_and_values.items():
        setvalue(graph, node, predicate, value)

def diff(graph1, graph2):
    return graph1 - graph2, graph2 - graph1

# CONTAINERS

LI_MATCH_PATTERN = re.compile(str(RDF) + "_([0-9]+)")
LI_CREATE_PATTERN = str(RDF) + "_{0}"

def isContainerItemPredicate(uri):
    match = LI_MATCH_PATTERN.match(uri)
    return int(match.group(1)) if match else None

def makeContainerItemPredicate(index):
    return LI_CREATE_PATTERN.format(index)

def getContainerStatements(graph, source, predicate):
    containers = list(graph.objects(URI(source), predicate))
    n = len(containers)
    if n == 1:
        return sorted([statement for statement in graph.triples((containers[0], None, None))
                       if isContainerItemPredicate(statement[1])],
                      key=lambda tr: tr[1])
    elif n == 0:
        return None
    else:
        raise ValueError("Expected only one value for {0}".format(predicate))

def getContainerItems(graph, node, predicate):
    statements = getContainerStatements(graph, node, predicate)
    return [statement[2] for statement in statements] if statements else None

def setContainerItems(graph, node, predicate, values, newtype=RDF.Seq):
    # Having to write code like this is a clear indication that triples are the wrong
    # abstraction for graphs, way too low level. Just sayin'.
    if values:
        statements = getContainerStatements(graph, node, predicate)
        if statements:
            container = statements[0][0]
            for statement in statements:
                graph.remove(statement)
        else:
            container = BNode()
            graph.add((node, predicate, container))
            graph.add((container, RDF.type, newtype))
        i = 1
        for value in values:
            graph.add((container, URIRef(makeContainerItemPredicate(i)), value))
            i += 1
    else:
        container = getvalue(graph, node, predicate)
        if container:
            graph.remove((node, predicate, container))
            graph.remove((container, None, None))

# FOCUSED GRAPH
#
# Instances of FocusedGraph have a specified "focus node".

class FocusedGraph(Graph):
    def __init__(self, focus=None, **kwargs):
        super().__init__(**kwargs)
        self._focus = focus or self.findFocus(**kwargs)

    @property
    def focus(self):
        return self._focus

    def findFocus(self, **kwargs):
        raise NotImplementedError()

    def getvalue(self, predicate):
        return getvalue(self, self._focus, predicate)

    def setvalue(self, predicate, value):
        setvalue(self, self._focus, predicate, value)

# SPARQL REPOSITORY

class SPARQLRepository(TemplatedQueryMixin, SPARQLUpdateStore):
    def __init__(self, query_endpoint=None, update_endpoint=None, **kwargs):
        super().__init__(query_endpoint=query_endpoint,
                         update_endpoint=update_endpoint or query_endpoint,
                         **kwargs)

    # Why do I get a complaint about this? SPARQLUpdateStore is not an abstract class...
    def triples_choices(self, _, context=None):
        pass

# JOURNALED GRAPH
#
# Instances of JournaledGraph keep a list of modifications (additions and deletions) and are
# capable of "flushing" these modifications to a backing store with a SPARQL endpoint.

class JournaledGraph(Graph):
    def __init__(self, store : SPARQLUpdateStore=None):
        super().__init__()
        self._journal = list()
        self._store = store

    def add(self, triple):
        super().add(triple)
        self._journal.append((True, triple))
        return self

    def remove(self, triple):
        super().remove(triple)
        self._journal.append((False, triple))
        return self

    def addN(self, quads):
        raise NotImplementedError()

    def flush(self, context=None):
        if self._store is None:
            raise ValueError("{g} has no store, but flush() called".format(g=self))
        if len(self._journal) > 0:
            if context is None:
                add_update = "INSERT DATA { $stuff }"
                remove_update = "DELETE DATA { $stuff }"
            else:
                add_update = "INSERT DATA { GRAPH $context { $stuff } }"
                remove_update = "DELETE DATA { GRAPH $context { $stuff } }"
            mods = list()
            case = self._journal[0][0]
            current_mods = Graph()
            for added, triple in self._journal:
                if added != case:
                    mods.append((case, current_mods))
                    case = added
                    current_mods = Graph()
                current_mods.add(triple)
            mods.append((case, current_mods))
            self._store.update(";".join([Templated.convert(add_update if added else remove_update,
                                                           {"stuff": self.ntriples(triples),
                                                            "context": context})
                                         for added, triples in mods]))  # no replacement necessary
            self._journal = list()

    @staticmethod
    def ntriples(graph):
        return graph.serialize(format="ntriples", encoding="ascii").decode()
