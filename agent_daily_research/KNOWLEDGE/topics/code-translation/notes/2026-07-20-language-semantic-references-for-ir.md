# Authoritative Per-Language Semantic References for Code-Translation IR Design

## Summary

There is no single cross-language authority that catalogues the semantic differences among Java, COBOL, Python, VBA, R, and SAS. The authoritative primary sources are each language's own reference specification. This note collects those specifications as the foundational inputs for designing an intermediate representation (IR) that must span these languages. It answers active question Q-2026-07-17-008 with reusable references rather than a fresh-news item; it was captured because code translation again had no fresh in-window primary update on 2026-07-20.

## Why It Matters

Q-2026-07-17-008 (priority 9) asks for resources that exhaustively document the semantic differences among these languages for IR design, and Q-2026-07-17-007 asks how to design a universal-yet-integrated IR. The hardest IR-design gaps are exactly the constructs these specs define and that have no clean analog across languages: COBOL fixed-point decimal (`PIC`/`USAGE`, `COMP`) data layout and `PERFORM` control flow; the SAS DATA step's program data vector, implicit iteration, and BY-group processing; R's lazy evaluation (promises) and copy-on-modify semantics; VBA's `Variant` dynamic typing; Java's static type system and memory model; and Python's dynamic object/data model. Any universal IR must represent or explicitly lose these behaviors, so the per-language specs are the primary evidence a design must reconcile.

## Evidence

- **Java** — [The Java Language Specification (JLS), Java SE 26](https://docs.oracle.com/javase/specs/) (index; SE 26 released 2026-03). Confidence: high; re-verified live 2026-07-20. Definitive for typing, evaluation order, and the memory model.
- **Python** — [The Python Language Reference](https://docs.python.org/3/reference/) (3.14). Confidence: high; re-verified live 2026-07-20. Covers the data model and execution model; explicitly the language semantics, not the standard library.
- **R** — [The R Language Definition](https://cran.r-project.org/doc/manuals/r-release/R-lang.html) (R 4.6.1). Confidence: high; re-verified live 2026-07-20. Documents promise objects/lazy evaluation, scoping, and copy-on-modify.
- **COBOL** — [IBM Enterprise COBOL for z/OS 6.4 Language Reference, SC27-8713-03](https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf). Confidence: high; verified in the research pass. Authoritative for the mainframe dialect that dominates legacy migration (`PERFORM`, `PIC`/`USAGE`, `COMP`, CICS/IMS/SQL interfaces). The vendor-neutral standard is ISO/IEC 1989:2023.
- **VBA** — [[MS-VBAL]: VBA Language Specification](https://learn.microsoft.com/en-us/openspecs/microsoft_general_purpose_programming_languages/ms-vbal/d5418146-0bd2-45eb-9c7a-fd9502722c74). Confidence: high; verified in the research pass. Microsoft's open specification defining VBA 7.x syntax and static/runtime semantics.
- **SAS** — [SAS 9.4 Language Reference: Concepts, Sixth Edition](https://documentation.sas.com/doc/en/lrcon/9.4/titlepage.htm). Confidence: high; confirmed via search 2026-07-20. Authoritative for DATA-step concepts (program data vector, implicit loop, BY-group processing).

## Uncertainties

- These are per-language references; the cross-language *differences* must be synthesized by the reader — no single authoritative "semantic differences" document exists for this exact language set.
- Spec editions drift (e.g. JLS tracks the current Java SE, Python tracks the current 3.x); the versions above are current as of 2026-07-20 and should be re-checked for later work.
- Secondary analyses (e.g. arXiv:2507.23356 on COBOL→Java transformation, from ~2025-07) enumerate specific verification points but are interpretation, not primary specification.

## Related Questions

- Q-2026-07-17-008 (resources documenting semantic differences among Java, COBOL, Python, VBA, R, SAS)
- Q-2026-07-17-007 (designing an ecosystem-integrated yet universal IR)
