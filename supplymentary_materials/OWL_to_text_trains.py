
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, BNode

# Load the OWL ontology file
g = Graph()
g.parse("trains/trains2.owl", format="xml")  # Change format if necessary (e.g., "turtle", "nt")

# Define common namespaces (update based on your ontology)
EX = Namespace("http://example.com/trains#")  # Modify this to match your ontology's namespace
IGNORED_PROPERTIES = {OWL.versionInfo, OWL.priorVersion, OWL.imports, RDF.type, RDF.first, RDF.rest}  # Ignore metadata & RDF list properties

# Function to extract and format RDF triples as structured text
def extract_triples(graph):
    structured_text = []

    # Extract classes and subclasses
    for s, o in graph.subject_objects(RDFS.subClassOf):
        if isinstance(s, BNode) or isinstance(o, BNode):  
            continue  # Skip blank nodes
        structured_text.append(f"The class '{s.split('#')[-1]}' is a subclass of class '{o.split('#')[-1]}'.")

    # Extract properties and their domains/ranges
    for p, o in graph.subject_objects(RDFS.domain):
        structured_text.append(f"The property '{p.split('#')[-1]}' applies to instances of '{o.split('#')[-1]}'.")

    for p, o in graph.subject_objects(RDFS.range):
        structured_text.append(f"The property '{p.split('#')[-1]}' has values of type '{o.split('#')[-1]}'.")

    # Extract individuals (instances of classes), excluding owl:Ontology
    for s, o in graph.subject_objects(RDF.type):
        if o not in [OWL.Class, RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.Ontology] and not isinstance(s, BNode):
            structured_text.append(f"'{s.split('#')[-1]}' is an instance of class '{o.split('#')[-1]}'.")

    # Extract object property relationships (excluding metadata & list properties)
    for s, p, o in graph.triples((None, None, None)):
        if p in IGNORED_PROPERTIES or isinstance(o, Namespace) or isinstance(s, BNode) or isinstance(o, BNode):
            continue  # Skip ignored properties & blank nodes
        
        structured_text.append(f"'{s.split('#')[-1]}' has a relationship '{p.split('#')[-1]}' with '{o.split('#')[-1]}'.")

    return structured_text

# Generate structured text from ontology
structured_text_output = extract_triples(g)

# Print structured knowledge
for sentence in structured_text_output:
    print(sentence)
