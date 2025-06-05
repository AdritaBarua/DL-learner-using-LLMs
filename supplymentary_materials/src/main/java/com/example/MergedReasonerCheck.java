package com.example;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.formats.PrefixDocumentFormat;
import org.semanticweb.owlapi.reasoner.*;
import org.semanticweb.owlapi.util.mansyntax.ManchesterOWLSyntaxParser;
import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;
import org.semanticweb.owlapi.expression.OWLEntityChecker;
import org.semanticweb.owlapi.util.DefaultPrefixManager;
import org.semanticweb.owlapi.util.SimpleShortFormProvider;
import org.semanticweb.owlapi.util.ShortFormProvider;
import org.semanticweb.owlapi.util.BidirectionalShortFormProviderAdapter;
import org.semanticweb.owlapi.expression.ShortFormEntityChecker;

import org.dllearner.kb.OWLAPIOntology;
import org.dllearner.reasoning.OWLAPIReasoner;
import org.dllearner.reasoning.ClosedWorldReasoner;
import org.dllearner.core.ComponentInitException;
import org.dllearner.core.ReasoningMethodUnsupportedException;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Main entry point: wraps DL‑Learner’s ClosedWorldReasoner (relocated into com.example.dllearner)
 * with a simple command‑line driver.
 */
public class MergedReasonerCheck {

    private final ClosedWorldReasoner cwr;

    public MergedReasonerCheck(OWLOntology ont) throws ComponentInitException {
        // initialize DL‑Learner’s Closed‑World wrapper (backed by Pellet)
        OWLAPIOntology dlOnt = new OWLAPIOntology(ont);
        OWLAPIReasoner dlBase = new OWLAPIReasoner(Set.of(dlOnt));
        dlBase.init();
        this.cwr = new ClosedWorldReasoner(dlBase);
        this.cwr.init();
    }

    public boolean hasType(OWLClassExpression expr, OWLNamedIndividual ind)
            throws ReasoningMethodUnsupportedException {
        return cwr.hasTypeImpl(expr, ind);
    }

    public static void main(String[] args) throws Exception {
        // === BEGIN: only new code to filter out those warning‐lines ===
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "error");
        System.setProperty("org.slf4j.simpleLogger.log.org.semanticweb.owlapi", "error");
        System.setProperty("org.slf4j.simpleLogger.log.com.clarkparsia", "error");
        System.setErr(new PrintStream(new OutputStream() {
            @Override public void write(int b) { /* no‑op */ }
        }));

        final PrintStream realOut = System.out;
        System.setOut(new PrintStream(new OutputStream() {
            private final StringBuilder buf = new StringBuilder();
            @Override
            public void write(int b) throws IOException {
                buf.append((char)b);
                if (b == '\n') {
                    String line = buf.toString();
                    buf.setLength(0);
                    // drop parser warnings and the "No instantiation found" line
                    if (!line.contains("entityExpansionLimit")
                     && !line.contains("not supported by parser type")
                     && !line.contains("No instantiation found for")) {
                        realOut.print(line);
                    }
                }
            }
        }, true));
        // === END: filtering code ===


        // === install a global whitelist filter on System.out ===
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(new OutputStream() {
            private final StringBuilder buf = new StringBuilder();
            @Override public void write(int b) throws IOException {
                buf.append((char)b);
                if (b == '\n') {
                    String line = buf.toString();
                    buf.setLength(0);
                    // only allow lines that start with these prefixes:
                    if (line.startsWith("--- Expr")
                     || line.startsWith("LLM expr:")
                     || line.startsWith("Reported accuracy:")
                     || line.startsWith("Positive ex.")
                     || line.startsWith("Negative ex.")
                     || line.startsWith("Reasoner accuracy")
                     || line.startsWith("Expr ")
                     || line.startsWith("=== Overall accuracy")
                     || line.startsWith("Reasoner: Pellet")
                     || line.startsWith("Usage: ")) {
                        originalOut.print(line);
                    }
                }
            }
        }, true));
        // optionally suppress System.err as well:
        System.setErr(originalOut);

        
        if (args.length != 5) {
            System.out.println("Usage: java -jar target/merged-reasoner-check-1.0-SNAPSHOT.jar ontology.owl http://www.ontology.org/onto# - PositiveExamples(e.g. p1,p2) NegativeExamples(e.g n1,n2) <<EOF <newline> class expression <newline> EOF");
            System.exit(1);
        }
        String ontPath = args[0], base = args[1], llmFile = args[2];
        String posList = args[3], negList = args[4];
        if (!base.endsWith("#") && !base.endsWith("/")) base += "#";

        // 1) Load ontology
        OWLOntologyManager mgr = OWLManager.createOWLOntologyManager();
        OWLOntology ont = mgr.loadOntologyFromOntologyDocument(new File(ontPath));
        OWLDocumentFormat fmt = mgr.getOntologyFormat(ont);
        if (fmt instanceof PrefixDocumentFormat) {
            ((PrefixDocumentFormat) fmt).setDefaultPrefix(base);
            mgr.setOntologyFormat(ont, fmt);
        }

        // 2) Initialize reasoner wrapper
        MergedReasonerCheck checker = new MergedReasonerCheck(ont);

        // 3) Prepare Manchester parser
        ManchesterOWLSyntaxParser parser = OWLManager.createManchesterParser();
        parser.setDefaultOntology(ont);

        // 4) Build your two‑arg adapter for everything declared in the ontology
        ShortFormProvider sfProvider = new SimpleShortFormProvider();
        BidirectionalShortFormProviderAdapter bidi =
            new BidirectionalShortFormProviderAdapter(
                Collections.singleton(ont),
                sfProvider
            );

        // now wrap it, *but* intercept “Thing”/“Nothing” to map to the built‑in OWL classes
        ShortFormEntityChecker baseChecker = new ShortFormEntityChecker(bidi);
        OWLDataFactory dfLocal = mgr.getOWLDataFactory();

        parser.setOWLEntityChecker(new OWLEntityChecker() {
            @Override
            public OWLClass getOWLClass(String name) {
                // recognize built‑ins
                if ("Thing".equals(name) || "owl:Thing".equals(name)) {
                    return dfLocal.getOWLThing();
                }
                if ("Nothing".equals(name) || "owl:Nothing".equals(name)) {
                    return dfLocal.getOWLNothing();
                }
                // otherwise defer to the normal short‑form checker
                return baseChecker.getOWLClass(name);
            }
            @Override public OWLObjectProperty    getOWLObjectProperty(String name)    { return baseChecker.getOWLObjectProperty(name); }
            @Override public OWLDataProperty      getOWLDataProperty(String name)      { return baseChecker.getOWLDataProperty(name); }
            @Override public OWLNamedIndividual   getOWLIndividual(String name)        { return baseChecker.getOWLIndividual(name); }
            @Override public OWLDatatype          getOWLDatatype(String name)          { return baseChecker.getOWLDatatype(name); }
            @Override public OWLAnnotationProperty getOWLAnnotationProperty(String name) { return baseChecker.getOWLAnnotationProperty(name); }
        });



        // 5) Restore normal output and print reasoner header
        System.out.println("Reasoner: Pellet");


        // 6) Parse positive/negative individual lists
        OWLDataFactory df = mgr.getOWLDataFactory();
        Set<OWLNamedIndividual> positives = new HashSet<>();
        for (String n : posList.split(",")) {
            String id = n.trim();
            if (!id.isEmpty()) positives.add(df.getOWLNamedIndividual(IRI.create(base + id)));
        }
        Set<OWLNamedIndividual> negatives = new HashSet<>();
        for (String n : negList.split(",")) {
            String id = n.trim();
            if (!id.isEmpty()) negatives.add(df.getOWLNamedIndividual(IRI.create(base + id)));
        }

        // 7) Read LLM expressions
        List<String> lines = "-".equals(llmFile)
            ? new BufferedReader(new InputStreamReader(System.in)).lines().toList()
            : Files.readAllLines(Paths.get(llmFile));

        int sumCorr = 0, sumTot = 0, perfect = 0, counter = 0, count = 0;

        for (String line : lines) {
            if (line.isBlank()) continue;

            // 1) normalize dashes
            String norm = line.replaceAll("[\u2010\u2011\u2012\u2013\u2014\u2212]", "-");

            // 2) strip trailing metrics‑paren only if it really is metrics
            String exprLine = norm;
            String metrics  = "";
            Pattern trailing = Pattern.compile("\\(([^)]+)\\)\\s*$");
            Matcher cm = trailing.matcher(norm);
            if(cm.find()) {
                String inner = cm.group(1).trim();
                if(inner.toLowerCase().matches("^(pred\\.\\s*acc\\.?|accuracy).*")) {
                    metrics  = inner;
                    exprLine = norm.substring(0, cm.start()).trim();
                }
            }

            // 3) split off "N: raw"
            String idx, raw;
            Matcher m2 = Pattern.compile("^\\s*(\\d+)\\s*:\\s*(.+)$").matcher(exprLine);
            if (m2.matches()) {
                idx = m2.group(1);
                raw = m2.group(2);
            } else {
                raw = exprLine.trim();
                idx = Integer.toString(++counter);
            }

            // 4) extract accuracy/F‑measure from metrics 
            boolean hasAcc = false, hasF = false;
            double rAcc = 0, fMeas = 0;
            if (!metrics.isEmpty()) {
                Matcher mAcc = Pattern.compile("(?i)(?:pred\\.\\s*acc\\.?|accuracy)\\s*:?[ ]*([0-9]+(?:\\.[0-9]+)?)%")
                                    .matcher(metrics);
                if (mAcc.find()) {
                    rAcc = Double.parseDouble(mAcc.group(1));
                    hasAcc = true;
                }
                Matcher mF = Pattern.compile("(?i)F-?measure\\s*:?[ ]*([0-9]+(?:\\.[0-9]+)?)%")
                                .matcher(metrics);
                if (mF.find()) {
                    fMeas = Double.parseDouble(mF.group(1));
                    hasF  = true;
                }
            }

            // 5) now raw contains your full LLM expression, e.g.
            //    "Train and (hasCar some (ShortCar and (loadCount value one)))"
            System.out.println("\n--- Expr " + idx + " ---");
            System.out.println("LLM expr: " + raw);
            if (hasAcc) System.out.printf("Reported accuracy: %.2f%%%n", rAcc);
            if (hasF)   System.out.printf("F-measure: %.2f%%%n", fMeas);


            // inject prefix block + preprocess
            parser.setStringToParse(raw);
            OWLClassExpression cls = parser.parseClassExpression();

            int okP = 0, okN = 0;
            for (OWLNamedIndividual ind : positives) {
                boolean ent = checker.hasType(cls, ind);
                System.out.println("Positive ex. " + ind.getIRI().getFragment() + " -> " + ent);
                if (ent) okP++;
            }
            for (OWLNamedIndividual ind : negatives) {
                boolean ent = checker.hasType(cls, ind);
                System.out.println("Negative ex. " + ind.getIRI().getFragment() + " -> " + ent);
                if (!ent) okN++;
            }

            int total = positives.size() + negatives.size();
            int correct = okP + okN;
            double acc = 100.0 * correct / total;
            System.out.printf("Reasoner accuracy for expr %s: %.2f%% (%d/%d correct)%n",
                            idx, acc, correct, total);
            if (correct == total) {
                System.out.println("Expr " + idx + " is VALID.");
                perfect++;
            } else {
                System.out.println("Expr " + idx + " is INVALID.");
            }
            sumCorr += correct;
            sumTot  += total;
            count++;
        }

        if (sumTot > 0) {
            double overall = 100.0 * perfect / count;
            System.out.printf("%n=== Overall accuracy: %.2f%%%n", overall);
        }
        System.exit(perfect > 0 ? 0 : 2);

    }
}
