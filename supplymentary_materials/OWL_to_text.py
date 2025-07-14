#!/usr/bin/env python
# coding: utf-8

# In[63]:


from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

# Load the OWL ontology file
g = Graph()
g.parse("basicFamily.owl", format="xml")  # Change format if necessary (e.g., "turtle", "nt")

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
    


# In[74]:


from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, BNode

# Load the OWL ontology file
g = Graph()
g.parse("/Users/adrita/Downloads/test_DL_learner/trains/trains2.owl", format="xml")  # Change format if necessary (e.g., "turtle", "nt")

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


# In[7]:


from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

# Load the OWL ontology file
g = Graph()
g.parse("/Users/adrita/Downloads/test_DL_learner/family-benchmark/family-benchmark.owl", format="xml")  # Change format if necessary (e.g., "turtle", "nt")

# Define common namespaces (update based on your ontology)
EX = Namespace("http://www.benchmark.org/family#")  # Modify this to match your ontology's namespace
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


# In[ ]:


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


# In[67]:


#prompt 1 (family.owl)
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("kb:Dino", "kb:Luigi", "kb:Mauro", "kb:Francesco", "kb:Giuseppe")

                And the negative examples are:
                ("kb:Antonella", "kb:Giovanna", "kb:Maria", "kb:Marisella", "kb:Milly", "kb:Nella", "kb:NonnaLina", "kb:Ombretta", "kb:Rosanna", "kb:Serena", "kb:Valentina", "kb:Luca")

                Then the complex class expression generated by DL-Learner for 'Brother' is:
                Male and (hasSibling some Thing) 
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                Complex class expression for {base_name}:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "positive"
negative_folder = "negative"
output_folder = "responses"
kb_file = "KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[1]:


#prompt 1 (family.owl) changed relations 
# Daughter -> Son
# Father -> Mother 
# GrandFather -> GrandMother 
# GrandMother -> GrandFather
# GrandParent -> Uncle
# Offspring -> Aunt
# Parent -> Children 
# Sibling -> Friend
# Sister -> Brother
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("kb:Dino", "kb:Luigi", "kb:Mauro", "kb:Francesco", "kb:Giuseppe")

                And the negative examples are:
                ("kb:Antonella", "kb:Giovanna", "kb:Maria", "kb:Marisella", "kb:Milly", "kb:Nella", "kb:NonnaLina", "kb:Ombretta", "kb:Rosanna", "kb:Serena", "kb:Valentina", "kb:Luca")

                Then the complex class expression generated by DL-Learner for 'Sister' based on the knowledge base is:
                Male and (hasSibling some Thing) 
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                Complex class expression for {base_name}:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "positive_changed_relations"
negative_folder = "negative_changed_relations"
output_folder = "responses_changed_relations"
kb_file = "KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[9]:


#prompt 1 (family-benchmark.owl)
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("ex:F2M13", "ex:F2M18", "ex:F2M11", "ex:F2M32", "ex:F3M44", "ex:F3M45", "ex:F5M64", "ex:F6M71", "ex:F6M81", "ex:F6M90", "ex:F6M100", "ex:F6M92", "ex:F7M113", "ex:F7M117", "ex:F7M115", "ex:F7M125", "ex:F7M123", "ex:F7M131", "ex:F9M151", "ex:F9M153", "ex:F9M159", "ex:F9M166", "ex:F9M162", "ex:F9M157", "ex:F9M167", "ex:F10M173", "ex:F10M183", "ex:F10M184", "ex:F10M188", "ex:F10M199")

                And the negative examples are:
                ("ex:F10M196", "ex:F1M8", "ex:F7F103", "ex:F3F41", "ex:F1M1", "ex:F9F164", "ex:F9M149", "ex:F9M147", "ex:F9F158", "ex:F2F12", "ex:F1F5", "ex:F6M88", "ex:F7M104", "ex:F7M109", "ex:F7M120", "ex:F6F83", "ex:F6M78", "ex:F3M47", "ex:F10F174", "ex:F6F76", "ex:F2F26", "ex:F6F89", "ex:F3M50", "ex:F3F42", "ex:F6F79", "ex:F10M194", "ex:F2F19", "ex:F2F24", "ex:F9F154", "ex:F4F58")

                Then the complex class expression generated by DL-Learner for 'Brother' based on the knowledge base is:
                Male and (hasSibling some Thing) 
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                Complex class expression for {base_name}:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/positive"
negative_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/negative"
output_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/responses"
kb_file = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/KB_family-benchmark.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[5]:


#prompt 1 (family.owl) without base name

import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("kb:Dino", "kb:Luigi", "kb:Mauro", "kb:Francesco", "kb:Giuseppe")

                And the negative examples are:
                ("kb:Antonella", "kb:Giovanna", "kb:Maria", "kb:Marisella", "kb:Milly", "kb:Nella", "kb:NonnaLina", "kb:Ombretta", "kb:Rosanna", "kb:Serena", "kb:Valentina", "kb:Luca")

                Then the complex class expression generated by DL-Learner is:
                Male and (hasSibling some Thing) 
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                The complex class expression is:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "positive"
negative_folder = "negative"
output_folder = "responses_without_basename"
kb_file = "KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[10]:


#prompt 1 (family-benchmark.owl) without basename
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("ex:F2M13", "ex:F2M18", "ex:F2M11", "ex:F2M32", "ex:F3M44", "ex:F3M45", "ex:F5M64", "ex:F6M71", "ex:F6M81", "ex:F6M90", "ex:F6M100", "ex:F6M92", "ex:F7M113", "ex:F7M117", "ex:F7M115", "ex:F7M125", "ex:F7M123", "ex:F7M131", "ex:F9M151", "ex:F9M153", "ex:F9M159", "ex:F9M166", "ex:F9M162", "ex:F9M157", "ex:F9M167", "ex:F10M173", "ex:F10M183", "ex:F10M184", "ex:F10M188", "ex:F10M199")

                And the negative examples are:
                ("ex:F10M196", "ex:F1M8", "ex:F7F103", "ex:F3F41", "ex:F1M1", "ex:F9F164", "ex:F9M149", "ex:F9M147", "ex:F9F158", "ex:F2F12", "ex:F1F5", "ex:F6M88", "ex:F7M104", "ex:F7M109", "ex:F7M120", "ex:F6F83", "ex:F6M78", "ex:F3M47", "ex:F10F174", "ex:F6F76", "ex:F2F26", "ex:F6F89", "ex:F3M50", "ex:F3F42", "ex:F6F79", "ex:F10M194", "ex:F2F19", "ex:F2F24", "ex:F9F154", "ex:F4F58")

                Then the complex class expression generated by DL-Learner based on the knowledge base is:
                Male and (hasSibling some Thing) 
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                The complex class expression is:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/positive"
negative_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/negative"
output_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/responses_without_basename"
kb_file = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/KB_family-benchmark.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[2]:


#prompt 1 (o3-mini) family_changed_relations
# Daughter -> Son
# Father -> Mother 
# GrandFather -> GrandMother 
# GrandMother -> GrandFather
# GrandParent -> Uncle
# Offspring -> Aunt
# Parent -> Children 
# Sibling -> Friend
# Sister -> Brother
import os
import openai

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key='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')

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def ask_question(prompt):    
    completion = client.chat.completions.create(
        model="o3-mini",
        reasoning_effort="high",
        messages=[{"role": "user", "content": prompt}],
        store=True,
    )
    return completion.choices[0].message.content.strip()

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read file contents
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.
                Use the Manchester syntax for the complex class expressions. 
                
                For example, if the positive examples are: 
                (\"kb:Dino\", \"kb:Luigi\", \"kb:Mauro\", \"kb:Francesco\", \"kb:Giuseppe\")  
                
                And the negative examples are: 
                (\"kb:Antonella\", \"kb:Giovanna\", \"kb:Maria\", \"kb:Marisella\", \"kb:Milly\", \"kb:Nella\", \"kb:NonnaLina\", \"kb:Ombretta\", \"kb:Rosanna\", \"kb:Serena\", \"kb:Valentina\", \"kb:Luca\"),  
                
                Then the complex class expression generated by DL-Learner for 'Sister' based on the knowlegde base is:
                Male and (hasSibling some Thing) 
                
                Now, find the complex class expressions for the following cases:
                Positive examples: {positive_text}  
                Negative examples: {negative_text}  
                Complex class expression for {base_name}:"""
                
                # Ask the model
                answer = ask_question(prompt)
                
                # Save response to a file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)
                
                print(f"Response saved to {response_file_path}")

# Define directories
positive_folder = "positive_changed_relations"
negative_folder = "negative_changed_relations"
output_folder = "responses_o3-mini_changed_relations"
kb_file = "KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)
process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[11]:


#prompt 1 (family-benchmark.owl) o3-mini
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):    
    completion = client.chat.completions.create(
        model="o3-mini",
        reasoning_effort="high",
        messages=[{"role": "user", "content": prompt}],
        store=True,
    )
    return completion.choices[0].message.content.strip()

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("ex:F2M13", "ex:F2M18", "ex:F2M11", "ex:F2M32", "ex:F3M44", "ex:F3M45", "ex:F5M64", "ex:F6M71", "ex:F6M81", "ex:F6M90", "ex:F6M100", "ex:F6M92", "ex:F7M113", "ex:F7M117", "ex:F7M115", "ex:F7M125", "ex:F7M123", "ex:F7M131", "ex:F9M151", "ex:F9M153", "ex:F9M159", "ex:F9M166", "ex:F9M162", "ex:F9M157", "ex:F9M167", "ex:F10M173", "ex:F10M183", "ex:F10M184", "ex:F10M188", "ex:F10M199")

                And the negative examples are:
                ("ex:F10M196", "ex:F1M8", "ex:F7F103", "ex:F3F41", "ex:F1M1", "ex:F9F164", "ex:F9M149", "ex:F9M147", "ex:F9F158", "ex:F2F12", "ex:F1F5", "ex:F6M88", "ex:F7M104", "ex:F7M109", "ex:F7M120", "ex:F6F83", "ex:F6M78", "ex:F3M47", "ex:F10F174", "ex:F6F76", "ex:F2F26", "ex:F6F89", "ex:F3M50", "ex:F3F42", "ex:F6F79", "ex:F10M194", "ex:F2F19", "ex:F2F24", "ex:F9F154", "ex:F4F58")

                Then the complex class expression generated by DL-Learner for 'Brother' based on the knowledge base is:
                Male and (hasSibling some Thing) 
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                Complex class expression for {base_name}:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/positive"
negative_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/negative"
output_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/responses_o3-mini"
kb_file = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/KB_family-benchmark.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[6]:


#prompt 1 (o3-mini) without base name

import os
import openai

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key='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')

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def ask_question(prompt):    
    completion = client.chat.completions.create(
        model="o3-mini",
        reasoning_effort="high",
        messages=[{"role": "user", "content": prompt}],
        store=True,
    )
    return completion.choices[0].message.content.strip()

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read file contents
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.
                Use the Manchester syntax for the complex class expressions. 
                
                For example, if the positive examples are: 
                (\"kb:Dino\", \"kb:Luigi\", \"kb:Mauro\", \"kb:Francesco\", \"kb:Giuseppe\")  
                
                And the negative examples are: 
                (\"kb:Antonella\", \"kb:Giovanna\", \"kb:Maria\", \"kb:Marisella\", \"kb:Milly\", \"kb:Nella\", \"kb:NonnaLina\", \"kb:Ombretta\", \"kb:Rosanna\", \"kb:Serena\", \"kb:Valentina\", \"kb:Luca\"),  
                
                Then the complex class expression generated by DL-Learner based on the knowlegde base is:
                Male and (hasSibling some Thing) 
                
                Now, find the complex class expressions for the following cases:
                Positive examples: {positive_text}  
                Negative examples: {negative_text}  
                The complex class expression is:"""
                
                # Ask the model
                answer = ask_question(prompt)
                
                # Save response to a file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)
                
                print(f"Response saved to {response_file_path}")

# Define directories
positive_folder = "positive"
negative_folder = "negative"
output_folder = "responses_o3-mini_without_basename"
kb_file = "KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)
process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[13]:


#prompt 1 (family-benchmark.owl) o3-mini without basename
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):    
    completion = client.chat.completions.create(
        model="o3-mini",
        reasoning_effort="high",
        messages=[{"role": "user", "content": prompt}],
        store=True,
    )
    return completion.choices[0].message.content.strip()

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("ex:F2M13", "ex:F2M18", "ex:F2M11", "ex:F2M32", "ex:F3M44", "ex:F3M45", "ex:F5M64", "ex:F6M71", "ex:F6M81", "ex:F6M90", "ex:F6M100", "ex:F6M92", "ex:F7M113", "ex:F7M117", "ex:F7M115", "ex:F7M125", "ex:F7M123", "ex:F7M131", "ex:F9M151", "ex:F9M153", "ex:F9M159", "ex:F9M166", "ex:F9M162", "ex:F9M157", "ex:F9M167", "ex:F10M173", "ex:F10M183", "ex:F10M184", "ex:F10M188", "ex:F10M199")

                And the negative examples are:
                ("ex:F10M196", "ex:F1M8", "ex:F7F103", "ex:F3F41", "ex:F1M1", "ex:F9F164", "ex:F9M149", "ex:F9M147", "ex:F9F158", "ex:F2F12", "ex:F1F5", "ex:F6M88", "ex:F7M104", "ex:F7M109", "ex:F7M120", "ex:F6F83", "ex:F6M78", "ex:F3M47", "ex:F10F174", "ex:F6F76", "ex:F2F26", "ex:F6F89", "ex:F3M50", "ex:F3F42", "ex:F6F79", "ex:F10M194", "ex:F2F19", "ex:F2F24", "ex:F9F154", "ex:F4F58")

                Then the complex class expression generated by DL-Learner based on the knowlegde base is:
                Male and (hasSibling some Thing) 
                
                Now, find the complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                The complex class expression is:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/positive"
negative_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/negative"
output_folder = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/responses_o3-mini_without_basename"
kb_file = "/Users/adrita/Downloads/test_DL_learner/family-benchmark/KB_family-benchmark.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[ ]:


#prompt 2 (family.owl)
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are:
                ("kb:Dino", "kb:Luigi", "kb:Mauro", "kb:Francesco", "kb:Giuseppe")

                And the negative examples are:
                ("kb:Antonella", "kb:Giovanna", "kb:Maria", "kb:Marisella", "kb:Milly", "kb:Nella", "kb:NonnaLina", "kb:Ombretta", "kb:Rosanna", "kb:Serena", "kb:Valentina", "kb:Luca")

                Then the complex class expressions generated by DL-Learner for 'Brother' are:
                Male and (hasSibling some Thing) (accuracy 100%, length 5, depth 1)
                Male and ((not (Male)) or (hasSibling some Thing)) (accuracy 100%, length 8, depth 1)
                Male and ((hasChild some Thing) or (hasSibling some Thing)) (accuracy 100%, length 9, depth 1)
                Male and ((hasSibling some Thing) or (hasSibling some Thing)) (accuracy 100%, length 9, depth 1)
                Male and ((hasSibling some Thing) or (hasParent max 1 Thing)) (accuracy 100%, length 10, depth 1)
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the shortest complex class expressions for the following cases:

                Positive examples: {positive_text}
                Negative examples: {negative_text}
                Shortest complex class expression for {base_name}:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "positive"
negative_folder = "negative"
output_folder = "responses_shortest"
kb_file = "KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[1]:


#prompt 1(trains2.owl)
import os
import openai

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

def process_files(positive_folder, negative_folder, output_folder, kb_file):
    """Iterate through all positive and negative files and save responses."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                # Read the contents of the positive and negative files
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file)
                # Construct the prompt question
                prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                For example, if the positive examples are: 
                (\"kb:east1\", \"kb:east2\", \"kb:east3\", \"kb:east4\", \"kb:east5\")  
                
                And the negative examples are: 
                (\"kb:west6\", \"kb:west7\", \"kb:west8\", \"kb:west9\", \"kb:west10\"),  
                
                Then the complex class expression generated by DL-Learner is: 
                hasCar some (ClosedCar and ShortCar) 
                
                Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:
                
                Positive examples: {positive_text}  
                Negative examples: {negative_text}  
                The complex class expression is:"""

                # Ask the question to the ChatGPT model
                answer = ask_question(prompt)

                # Store the response in a separate file
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "/Users/adrita/Downloads/test_DL_learner/trains/positive"
negative_folder = "/Users/adrita/Downloads/test_DL_learner/trains/negative"
output_folder = "/Users/adrita/Downloads/test_DL_learner/trains/responses"
kb_file = "/Users/adrita/Downloads/test_DL_learner/trains/KB_trains2.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file)


# In[8]:


import os
import re

def extract_examples(file_path):
    """Extracts positive and negative examples from a given file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract positive examples
    pos_match = re.search(r'lp\.positiveExamples = \{([\s\S]*?)\}', content)
    positive_examples = pos_match.group(1).strip().split(',') if pos_match else []
    
    # Extract negative examples
    neg_match = re.search(r'lp\.negativeExamples = \{([\s\S]*?)\}', content)
    negative_examples = neg_match.group(1).strip().split(',') if neg_match else []
    
    return [ex.strip().strip('"') for ex in positive_examples], [ex.strip().strip('"') for ex in negative_examples]

def process_files(directory):
    """Processes all files ending with 'celoe.txt' in the given directory."""
    for file_name in os.listdir(directory):
        if file_name.endswith('celoe.txt'):
            file_path = os.path.join(directory, file_name)
            base_name = file_name.split('_')[0]  # Extract the first word before '_'
            
            positive_examples, negative_examples = extract_examples(file_path)
            
            # Save positive examples
            with open(os.path.join(directory, f'positive_{base_name}.txt'), 'w', encoding='utf-8') as pos_file:
                pos_file.write('\n'.join(positive_examples))
            
            # Save negative examples
            with open(os.path.join(directory, f'negative_{base_name}.txt'), 'w', encoding='utf-8') as neg_file:
                neg_file.write('\n'.join(negative_examples))

if __name__ == "__main__":
    folder_path = '/Users/adrita/Downloads/test_DL_learner/family-benchmark/'  # Change this to the target folder path
    process_files(folder_path)


# In[ ]:


import OpenAI from "openai";
const openai = new OpenAI();

const prompt = `
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
`;
 
const completion = await openai.chat.completions.create({
  model: "o3-mini",
  reasoning_effort: "medium",
  messages: [
    {
      role: "user", 
      content: prompt
    }
  ],
  store: true,
});

console.log(completion.choices[0].message.content);


# In[23]:


import os
import openai
import subprocess

from openai import OpenAI
client = OpenAI(api_key='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')

# Function to read the text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to interact with ChatGPT and ask questions
def ask_question(prompt):
    response = client.chat.completions.create(
        model='gpt-4o',  # Use the appropriate GPT-4 model
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

# Function to validate OWL class expressions using HermiT or Pellet
def closed_world_reasoner(expression, kb_file):
    """
    Calls an external Java-based OWL reasoner (HermiT or Pellet) to check if the expression is valid.
    Returns True if valid, otherwise False with reasoner feedback.
    """
    reasoner_script = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/validate_expression.jar"  # Ensure this Java JAR file is created
    command = ["java", "-jar", reasoner_script, kb_file, expression]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        
        if "VALID" in output:
            return True, "Expression is valid according to the reasoner."
        else:
            return False, f"Reasoner feedback: {output}"
    except subprocess.CalledProcessError as e:
        return False, f"Error running reasoner: {e.stderr}"

def process_files(positive_folder, negative_folder, output_folder, kb_file_text):
    """Iterate through all positive and negative files, validate with reasoner, and refine if needed."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]  # Extract the main identifier
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")
            
            if os.path.exists(negative_file_path):
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file_text)
                
                attempts = 0
                max_attempts = 3
                valid_expression = False
                feedback = ""
                
                while attempts < max_attempts and not valid_expression:
                    # Construct the prompt question
                    prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                    Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                    For example, if the positive examples are:
                    (\"kb:Dino\", \"kb:Luigi\", \"kb:Mauro\", \"kb:Francesco\", \"kb:Giuseppe\")

                    And the negative examples are:
                    (\"kb:Antonella\", \"kb:Giovanna\", \"kb:Maria\", \"kb:Marisella\", \"kb:Milly\", \"kb:Nella\", \"kb:NonnaLina\", \"kb:Ombretta\", \"kb:Rosanna\", \"kb:Serena\", \"kb:Valentina\", \"kb:Luca\")

                    Then the complex class expression generated by DL-Learner is:
                    Male and (hasSibling some Thing)
                    
                    Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions for the following cases:
                    
                    Positive examples: {positive_text}
                    Negative examples: {negative_text}
                    {feedback} 
                    The complex class expression is:"""

                    answer = ask_question(prompt)

                    # Validate using the reasoner
                    valid_expression, reasoner_feedback = closed_world_reasoner(answer, kb_file)
                    feedback = f"\nThe previous answer was: {answer}. {reasoner_feedback} Please refine it." if not valid_expression else ""
                    
                    attempts += 1
                
                # Store the final response
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                print(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/positive"
negative_folder = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/negative"
output_folder = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/responses_with_reasoner"
kb_file = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/basicFamily.owl"  # OWL file for ontology
kb_file_text = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

process_files(positive_folder, negative_folder, output_folder, kb_file_text)


# In[32]:


import os
import openai
import subprocess

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='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')

# Logging function
log_file = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/debug_log.txt"

# Ensure that debug_log.txt is a file, not a directory
if os.path.exists(log_file) and os.path.isdir(log_file):
    print(f"⚠️ Found a directory named {log_file}. Removing it...")
    os.rmdir(log_file)  # Remove the directory to create a file later


def log_message(message):
    """Logs messages to a file and prints them for debugging."""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)  # Also print to console

# Function to read a text file
def read_text_file(file_path):
    """Reads and returns content from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Function to query GPT-4
def ask_question(prompt):
    """Interacts with ChatGPT and returns a response."""
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0,
        top_p=1
    )
    response_text = response.choices[0].message.content.strip()
    log_message(f"\nGenerated Class Expression from LLM: {response_text}")
    return response_text

    
def closed_world_reasoner(expression, kb_file):
    """
    Calls an external Java-based OWL reasoner (HermiT) to check if the expression is valid.
    Returns True if valid, otherwise False with reasoner feedback.
    """
    reasoner_jar_path = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/"
    command = [
        "java", "-cp",
        f".:{reasoner_jar_path}HermiT.jar:{reasoner_jar_path}owlapi-distribution-3.5.6.jar:"
        f"{reasoner_jar_path}guava-18.0.jar:{reasoner_jar_path}trove4j-3.0.3.jar:"
        f"{reasoner_jar_path}validate_expression.jar",
        "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/OWLReasonerValidator",
        kb_file,
        expression
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        
        log_message(f"Reasoner Output: {output}")
        
        if "VALID" in output:
            return True, "Expression is valid according to the reasoner."
        else:
            return False, f"Reasoner feedback: {output}"
    
    except subprocess.CalledProcessError as e:
        log_message(f"Error running reasoner: {e.stderr}")
        return False, f"Error running reasoner: {e.stderr}"

# Function to process files and generate class expressions
def process_files(positive_folder, negative_folder, output_folder, kb_file_text, kb_file):
    """Iterates through files, queries LLM, validates expressions, and saves results."""
    for file_name in os.listdir(positive_folder):
        if file_name.startswith("positive_") and file_name.endswith(".txt"):
            base_name = file_name[len("positive_"):].split(".")[0]
            positive_file_path = os.path.join(positive_folder, file_name)
            negative_file_path = os.path.join(negative_folder, f"negative_{base_name}.txt")
            response_file_path = os.path.join(output_folder, f"response_{base_name}.txt")

            if os.path.exists(negative_file_path):
                positive_text = read_text_file(positive_file_path)
                negative_text = read_text_file(negative_file_path)
                kb_file_read = read_text_file(kb_file_text)

                attempts = 0
                max_attempts = 3
                valid_expression = False
                feedback = ""

                while attempts < max_attempts and not valid_expression:
                    prompt = f"""Take the given ontology as the knowledge base: {kb_file_read}.

                    Use this knowledge base to extract complex class expressions for the given positive and negative examples. A complex class expression is an OWL class expression that consists of the classes and properties that apply to the positive examples but not to the negative examples.

                    Example:
                    If the positive examples are:
                    ("kb:Dino", "kb:Luigi", "kb:Mauro", "kb:Francesco", "kb:Giuseppe")

                    And the negative examples are:
                    ("kb:Antonella", "kb:Giovanna", "kb:Maria", "kb:Marisella", "kb:Milly", "kb:Nella", "kb:NonnaLina", "kb:Ombretta", "kb:Rosanna", "kb:Serena", "kb:Valentina", "kb:Luca")

                    Then the complex class expression generated by DL-Learner is:
                    Male and (hasSibling some Thing)

                    Now, perform a logical analysis based on the knowledge base and the given examples to find the complex class expressions.
                    
                    Positive examples: {positive_text}
                    Negative examples: {negative_text}
                    {feedback} 
                    Don't give me any description just the final complex class expression: """

                    answer = ask_question(prompt)

                    if answer.strip():  # Ensure we don't pass empty responses
                        valid_expression, reasoner_feedback = closed_world_reasoner(answer, kb_file)
                    else:
                        reasoner_feedback = "LLM generated an empty response."
                        valid_expression = False

                    feedback = f"\nThe previous answer was: {answer}. {reasoner_feedback} Please refine it." if not valid_expression else ""

                    attempts += 1

                # Save the final valid (or last attempted) expression
                with open(response_file_path, 'w', encoding='utf-8') as response_file:
                    response_file.write(answer)

                log_message(f"Response saved to {response_file_path}")

# Define the directories
positive_folder = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/positive"
negative_folder = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/negative"
output_folder = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/responses_with_reasoner"
kb_file = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/basicFamily.owl"
kb_file_text = "/Users/adrita/Downloads/test_DL_learner/yinyang_examples/KB_family.txt"

# Create output directory if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Run the processing function
process_files(positive_folder, negative_folder, output_folder, kb_file_text, kb_file)


# In[7]:


import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.io.OWLParserException;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.util.DefaultPrefixManager;
import org.semanticweb.owlapi.util.SimpleShortFormProvider;
import org.semanticweb.owlapi.manchestersyntax.parser.ManchesterOWLSyntaxParser;

import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;

import java.io.File;
import java.util.HashSet;
import java.util.Set;

public class PelletReasoningTest {

   public static void main(String[] args) {
       try {
           # 1. Load the ontology
           OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
           # Change the file path to your ontology
           File ontologyFile = new File("path/to/your/ontology.owl");
           OWLOntology ontology = manager.loadOntologyFromOntologyDocument(ontologyFile);
           System.out.println("Ontology loaded: " + ontology.getOntologyID());

           # 2. Create the Pellet reasoner using the OWL API
           OWLReasonerFactory pelletFactory = PelletReasonerFactory.getInstance();
           OWLReasoner reasoner = pelletFactory.createReasoner(ontology);
           reasoner.precomputeInferences();

           # 3. Parse the complex class expression (Manchester syntax)
           # For example, suppose we want to test the expression: "ex:Parent and (hasChild some ex:Student)"
           String complexClassExprStr = "ex:Parent and (hasChild some ex:Student)";
           ## Define prefix mappings – adjust the base IRI as needed.
           DefaultPrefixManager prefixManager = new DefaultPrefixManager("http://example.com/ontology#");
           
           # Set up the Manchester parser
           ManchesterOWLSyntaxParser parser = OWLManager.createManchesterParser();
           parser.setDefaultOntology(ontology);
           parser.setStringToParse(complexClassExprStr);
           parser.setPrefixManager(prefixManager);
           OWLClassExpression complexClassExpr = parser.parseClassExpression();
           System.out.println("Parsed complex class expression: " + complexClassExpr);

           # 4. Define positive and negative example individuals
           OWLDataFactory dataFactory = manager.getOWLDataFactory();
           Set<OWLNamedIndividual> positiveExamples = new HashSet<>();
           positiveExamples.add(dataFactory.getOWLNamedIndividual(":Alice", prefixManager));
           positiveExamples.add(dataFactory.getOWLNamedIndividual(":Bob", prefixManager));

           Set<OWLNamedIndividual> negativeExamples = new HashSet<>();
           negativeExamples.add(dataFactory.getOWLNamedIndividual(":Charlie", prefixManager));
           negativeExamples.add(dataFactory.getOWLNamedIndividual(":David", prefixManager));

           # 5. Check satisfiability for positive examples:
           boolean allPositivesCorrect = true;
           for (OWLNamedIndividual ind : positiveExamples) {
               # Create a class assertion axiom: (complexClassExpr)(ind)
               OWLClassAssertionAxiom axiom = dataFactory.getOWLClassAssertionAxiom(complexClassExpr, ind);
               boolean isEntailed = reasoner.isEntailed(axiom);
               System.out.println("Positive example " + ind + " entailed: " + isEntailed);
               if (!isEntailed) {
                   allPositivesCorrect = false;
               }
           }

           # 6. Check that negative examples do NOT satisfy the expression:
           boolean allNegativesCorrect = true;
           for (OWLNamedIndividual ind : negativeExamples) {
               OWLClassAssertionAxiom axiom = dataFactory.getOWLClassAssertionAxiom(complexClassExpr, ind);
               boolean isEntailed = reasoner.isEntailed(axiom);
               System.out.println("Negative example " + ind + " entailed: " + isEntailed);
               if (isEntailed) {
                   allNegativesCorrect = false;
               }
           }

           # 7. Report results
           if (allPositivesCorrect && allNegativesCorrect) {
               System.out.println("SUCCESS: The class expression correctly covers all positive examples and excludes all negative examples.");
           } else {
               System.out.println("FAILURE: The class expression does not meet the criteria.");
           }

           # Dispose the reasoner when done
           reasoner.dispose();

       } catch (OWLOntologyCreationException | OWLParserException | OWLRuntimeException e) {
           e.printStackTrace();
       }
   }
}

