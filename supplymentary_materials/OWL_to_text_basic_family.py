
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

# Load the OWL ontology file
g = Graph()
g.parse("yinyang_examples/basicFamily.owl", format="xml")  # Change format if necessary (e.g., "turtle", "nt")

# Define common namespaces (update based on your ontology)
EX = Namespace("http://www.csc.liv.ac.uk/~luigi/ontologies/basicFamily/")  # Modify this to match your ontology's namespace
IGNORED_PROPERTIES = {OWL.versionInfo, OWL.priorVersion, OWL.imports, RDF.type}  # Metadata properties to ignore

# Function to extract and format RDF triples as structured text
def extract_triples(graph):
    structured_text = []

    # Extract classes and subclasses, ensuring 'Thing' is mentioned as the top class
    top_class_found = False
    for s, o in graph.subject_objects(RDFS.subClassOf):
        if o == OWL.Thing:
            top_class_found = True
        structured_text.append(f"The class '{s.split('#')[-1]}' is a subclass of class '{o.split('#')[-1]}'.")

    # Ensure that the root class 'Thing' is mentioned
    if not top_class_found:
        structured_text.append(f"The class '{OWL.Thing.split('#')[-1]}' is a top level class that includes everything. All other classes are subclass of '{OWL.Thing.split('#')[-1]}'.")

    # Extract properties and their domains/ranges
    for p, o in graph.subject_objects(RDFS.domain):
        structured_text.append(f"The property '{p.split('#')[-1]}' applies to instances of '{o.split('#')[-1]}'.")

    for p, o in graph.subject_objects(RDFS.range):
        structured_text.append(f"The property '{p.split('#')[-1]}' has values of type '{o.split('#')[-1]}'.")

    # Extract individuals (instances of classes), excluding owl:Ontology
    for s, o in graph.subject_objects(RDF.type):
        if o not in [OWL.Class, RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.Ontology]:
            structured_text.append(f"'{s.split('#')[-1]}' is an instance of class '{o.split('#')[-1]}'.")

    # Extract object property relationships (excluding metadata properties)
    for s, p, o in graph.triples((None, None, None)):
        if p not in IGNORED_PROPERTIES and not isinstance(o, Namespace) and o != OWL.Ontology:
            structured_text.append(f"'{s.split('#')[-1]}' has a relationship '{p.split('#')[-1]}' with '{o.split('#')[-1]}'.")

    return structured_text

# Generate structured text from ontology
structured_text_output = extract_triples(g)

# Print structured knowledge
for sentence in structured_text_output:
    print(sentence)
    

