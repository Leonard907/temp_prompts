from datasets import load_dataset
import json
import os

dt = load_dataset("shipWr3ck/supersummary", split="test")
all_claims = json.load(open("claims_dict.json"))

prompt = \
"""You are an annotator that verifies the faithfulness of statements made in a given summary of a book against the actual text of the book. Given the entire book text and a short claim, determine whether the claim is supported, not supported or not present in the book according to these guidelines:

1. Supported: The claim is directly supported by the text. Add a short explanation of why by giving specific evidence from the text.
2. Not Supported: The claim mentions a fact that clearly contradicts to the actual text. Add a short explanation of why by giving specific evidence from the text.
3. Not Present: The claim mentions a fact that is not present in the text. Add a short explanation of why in 1-2 sentences and try to include evidence that is similar to the claim but is fundamentally different.

Book Text: {book_text}

Claim: {claim}

Decision: 
"""

def split_claims(claim):
    lines = claim.split("\n")
    parsed_lines = []
    for line in lines:
        if line.startswith("- "):
            parsed_lines.append(line[2:].strip())
        elif line.strip() == "":
            continue
        else:
            parsed_lines.append(line.strip())
    return parsed_lines

for k in all_claims:
    claims = all_claims[k]
    for method in claims:
        claim = claims[method]
        parsed_facts = split_claims(claim)
        for i in range(len(parsed_facts)):
            prompt_text = prompt.format(book_text=dt[int(k)]['input'], claim=parsed_facts[i])
            # import pdb; pdb.set_trace()
            if "/" in method:
                method = method.split("plansumm/new_names/supersummary_70b_")[1].split(".json")[0]
            os.makedirs(str(k), exist_ok=True)
            with open(f"{k}/{method}_{i}.txt", "w") as f:
                f.write(prompt_text)