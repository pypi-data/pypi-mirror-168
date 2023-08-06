from rdflib import Literal, URIRef
import string
import numbers

def identity(x):
    return x

# Make a new dictionary with values mapped using a callable
def mapDict(dictionary, mapper=identity):
    d = dict()
    for key, value in dictionary.items():
        d[key] = mapper(value)
    return d

# TEMPLATED QUERIES
#
# This mechanism can be used in lieu of RDFLib's "initBindings=" parameter for SPARQL queries,
# with the added benefit that replacements are not limited to SPARQL terms.
class Templated:

    @classmethod
    def query(cls, graph, template, **kwargs):
        return graph.query(cls.convert(template, kwargs) if kwargs else template)

    @classmethod
    def update(cls, graph, template, **kwargs):
        graph.update(cls.convert(template, kwargs) if kwargs else template)

    @classmethod
    def convert(cls, template, kwargs):
        return string.Template(template).substitute(**mapDict(kwargs, mapper=cls.forSPARQL))

    @classmethod
    def forSPARQL(cls, thing):
        if isinstance(thing, URIRef):
            return "<" + str(thing) + ">"
        elif isinstance(thing, Literal):
            s = '"' + str(thing) + '"'
            if thing.datatype:
                return s + "^^<" + str(thing.datatype) + ">"
            elif thing.language:
                return s + "@" + thing.language
            else:
                return s
        elif isinstance(thing, str):
            return thing  # if thing[0] == '?' else cls.forSPARQL(Literal(thing))
        elif isinstance(thing, bool):
            return "true" if thing else "false"
        elif isinstance(thing, numbers.Number):
            return thing
        elif thing is None:
            return ""
        else:
            raise ValueError("Cannot make a SPARQL compatible value: %s", thing)

class TemplatedQueryMixin:  # abstract

    def query(self, querystring, **kwargs):
        return Templated.query(self, querystring, **kwargs)

    def update(self, querystring, **kwargs):
        Templated.update(self, querystring, **kwargs)
