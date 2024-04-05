from ..services.google import Prompt

prompt = Prompt(
    project_id="motorway-genai",
    location="us-central1",
    model_id="gemini-1.0-pro-001",
    temperature=0.9,
    max_output_tokens=2048,
    top_p=1,
    content="""
    
Given two sets of information extracted via OCR, you will compare the names and addresses in each set to determine if they match. Your evaluation should account for common OCR mistakes, such as misread characters or slight spelling errors that don't significantly alter the identity of the names or addresses. Your response should be structured in a JSON format with three fields: match, reason, and message.

Match: A boolean value (true or false) indicating whether the names and addresses match. Consider matches even if there are minor OCR-related errors that don't change the overall identity of the names or addresses.

Reason: This should detail why the names and addresses do not match. If they don't match, specify what elements are mismatched or if any common OCR errors might have led to discrepancies. For example, 'e' mistaken for 'c', 'l' for 'i', etc. If they match leave this blank.

Message: If there is a match, offer a super positive affirmation that this stage is complete using the person's name. Use in the message the full person's name by transforming it to a title case format.

If not, calmly but in a playful tone explain why and where the mismatch occurred. And generate a suggestion to review again the documents provided and try again.

Please ensure that your analysis is thorough yet considers the inherent inaccuracies that come with OCR text extraction. The goal is to identify genuine mismatches while overlooking minor discrepancies that do not affect the identification process.

{context}
Make sure always that your response adhere to the JSON format and fields are specified.

    """,
    variables={},
)
