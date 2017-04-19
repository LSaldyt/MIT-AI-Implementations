'''
The following formalist theory is offered as contrast to the logicistic theory of PM. A contemporary formal system would be constructed as follows:

    Symbols used: This set is the starting set, and other symbols can appear but only by definition from these beginning symbols. A starting set might be the following set derived from Kleene 1952: logical symbols "→" (implies, IF-THEN, "⊃"), "&" (and), "V" (or), "¬" (not), "∀" (for all), "∃" (there exists); predicate symbol "=" (equals); function symbols "+" (arithmetic addition), "∙" (arithmetic multiplication), "'" (successor); individual symbol "0" (zero); variables "a", "b", "c", etc.; and parentheses "(" and ")".[3]
    Symbol strings: The theory will build "strings" of these symbols by concatenation (juxtaposition).[4]
    Formation rules: The theory specifies the rules of syntax (rules of grammar) usually as a recursive definition that starts with "0" and specifies how to build acceptable strings or "well-formed formulas" (wffs).[5] This includes a rule for "substitution".[6] of strings for the symbols called "variables" (as opposed to the other symbol-types).
    Transformation rule(s): The axioms that specify the behaviours of the symbols and symbol sequences.
    Rule of inference, detachment, modus ponens : The rule that allows the theory to "detach" a "conclusion" from the "premises" that led up to it, and thereafter to discard the "premises" (symbols to the left of the line │, or symbols above the line if horizontal). If this were not the case, then substitution would result in longer and longer strings that have to be carried forward. Indeed, after the application of modus ponens, nothing is left but the conclusion, the rest disappears forever.

    Contemporary theories often specify as their first axiom the classical or modus ponens or "the rule of detachment":

        A, A ⊃ B │ B

    The symbol "│" is usually written as a horizontal line, here "⊃" means "implies". The symbols A and B are "stand-ins" for strings; this form of notation is called an "axiom schema" (i.e., there is a countable number of specific forms the notation could take). This can be read in a manner similar to IF-THEN but with a difference: given symbol string IF A and A implies B THEN B (and retain only B for further use). But the symbols have no "interpretation" (e.g., no "truth table" or "truth values" or "truth functions") and modus ponens proceeds mechanistically, by grammar alone. 
'''

def pm_branches(node):
    options = []
    return options
