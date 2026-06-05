import spacy
from spacy.matcher import Matcher
import gradio as gr

def strict_grammar_checker(text):
    if not text.strip():
        return "✨ Enter some text above to check its grammar syntax!"
        
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)
    errors = []

    # --- DEFINE NLP GRAMMAR PATTERNS ---
    # 1. Double Negative Rule
    matcher.add("DOUBLE_NEGATIVE", [[
        {"DEP": "neg"},
        {"OP": "*"},
        {"LOWER": {"IN": ["nothing", "nobody", "none", "no", "nowhere"]}}
    ]])

    # 2. Incorrect Past Participle after Auxiliary Verb
    matcher.add("BAD_PAST_PARTICIPLE", [[
        {"LOWER": {"IN": ["has", "have", "had", "been", "was", "were"]}},
        {"TAG": "VBD"} 
    ]])

    # 3. Strict Pronoun Mismatch: "You does / You is"
    matcher.add("YOU_MISMATCH", [[
        {"LOWER": "you"},
        {"LOWER": {"IN": ["does", "is", "has"]}}
    ]])

    # 4. Strict Pronoun Mismatch: "They/We does / They/We is"
    matcher.add("PLURAL_PRONOUN_MISMATCH", [[
        {"LOWER": {"IN": ["they", "we"]}},
        {"LOWER": {"IN": ["does", "is", "was"]}}
    ]])

    # 5. Strict Pronoun Mismatch for "I" (Catching "I are", "I is")
    matcher.add("I_PRONOUN_MISMATCH", [[
        {"LOWER": "i"},
        {"LOWER": {"IN": ["are", "is", "were"]}}
    ]])

    # Execute pattern matching
    matches = matcher(doc)
    
    for match_id, start, end in matches:
        rule_name = nlp.vocab.strings[match_id]
        span = doc[start:end]
        
        if rule_name == "DOUBLE_NEGATIVE":
            errors.append(f"❌ Double Negative found in '{span.text}'\n   💡 Fix: Remove one of the negative elements.")
        elif rule_name == "BAD_PAST_PARTICIPLE":
            errors.append(f"❌ Wrong verb tense in '{span.text}'\n   💡 Fix: Use the past participle form (V3) after auxiliary verbs.")
        elif rule_name in ("YOU_MISMATCH", "PLURAL_PRONOUN_MISMATCH"):
            errors.append(f"❌ Subject-Verb conflict in '{span.text}'\n   💡 Fix: Change the verb to its plural agreement form.")
        elif rule_name == "I_PRONOUN_MISMATCH":
            errors.append(f"❌ Subject-Verb conflict in '{span.text}'\n   💡 Fix: 'I' cannot pair with '{span[1].text}'. Use 'am' or 'was'.")

    # Format output results for UI display
    if not errors:
        return "✨ Passed all strict structural rules! Grammatically sound."
    
    return "\n\n".join(errors)

# --- GRADIO USER INTERFACE DESIGN ---
# Setting up a beautiful interface layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 AI Rule-Based Grammar Checker")
    gr.Markdown("An NLP application leveraging **spaCy** token stream analysis and pattern matching.")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Enter Your Sentence", 
                placeholder="Type here (e.g., 'i are good' or 'they does run')...",
                lines=3
            )
            submit_btn = gr.Button("Analyze Syntax", variant="primary")
            
        with gr.Column():
            output_report = gr.Textbox(
                label="NLP Grammatical Analysis Report", 
                lines=5,
                interactive=False
            )
            
    # Connect UI button action to backend processing logic
    submit_btn.click(fn=strict_grammar_checker, inputs=input_text, outputs=output_report)

# Launch the app inside Colab
demo.launch(debug=True)
