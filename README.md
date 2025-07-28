# LLM-Driven DL-Learner Framework

This repository contains supplementary materials and scripts used for evaluating Concept Induction in Description Logic(DL) class expressions through Large Language Models (LLMs).

## Contents

### 📁 Notebooks

#### `LLM_gen_DL-learner_with_resoner.ipynb`
This notebook demonstrates:
- Prompting LLMs (e.g., GPT-4, o3-mini) to generate DL class expressions.
- Construction of prompts with positive/negative examples and background knowledge.
- Automatic validation using a Java-based OWL reasoner.
- Logging of results including correctness and average processing time.

#### `OWL_to_text.ipynb`
This utility notebook:
- Converts OWL ontologies into human-readable natural language text.
- Is useful for prompt creation or manual inspection of ontology axioms.

#### Install dependencies

pip install -r requirements.txt

## ⚙️ Java OWL Reasoner

To validate generated class expressions with a symbolic reasoner, compile and invoke the following Java class:

#### `src/main/java/com/example/MergedReasonerCheck.java`

This script uses the [OWL API](https://github.com/owlcs/owlapi) and [Pellet](https://github.com/stardog-union/pellet) reasoner to:
- Parse class expressions in Manchester OWL syntax.
- Apply closed-world reasoning using user-defined positive/negative assertions. Closed world reasoning is invoked by calling the Closed World Reasoner class from [DL-Learner](https://github.com/AKSW/DL-Learner).
- Output validation results for class expressions produced by LLMs.

> 🔍 **Note:** Closed world reasoning is invoked by calling the Closed World Reasoner class from [DL-Learner](https://github.com/AKSW/DL-Learner).

### Build Instructions:
To generate the `.jar` file needed to run the reasoner:

```bash
cd supplymentary_materials
mvn clean package
```

This creates a JAR file typically at:
```
target/merged-reasoner-check-1.0-SNAPSHOT.jar
```

### Usage Example:

```bash
java -jar target/merged-reasoner-check-1.0-SNAPSHOT.jar \
  path/to/ontology.owl \
  http://your-ontology-base-uri# \
- \
  PositiveExample1,PositiveExample2 \
  NegativeExample1,NegativeExample2 <<EOF
  YourClassExpressionHere
EOF
```

## 📁 Dataset

The repository also contains folders such as `yinyang_examples` with:
- Different ontology configurations for the basicFamily.owl ontology(default, changed gender, changed relations).
- Positive/negative example sets.
- DL-Learner outputs.
- Reasoner validation outputs from different LLMs.

There are two other folders for family-benchmark.owl and trains2.owl ontologies. 


## 📌 Notes

- Ensure you have Java 11+ and Maven installed to compile the reasoner.
- LLM outputs are tested with reasoning-based verification for correctness.
- You may adapt the prompt structure and input formatting based on your ontology structure.
