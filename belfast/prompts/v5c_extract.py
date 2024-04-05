from ..services.google import Prompt

prompt = Prompt(
    project_id="motorway-genai",
    location="us-central1",
    model_id="gemini-1.0-pro-vision-001",
    temperature=0.2,
    max_output_tokens=2048,
    top_p=1,
    top_k=32,
    content="""
    
You are a document entity extraction specialist. Given a document, your task is to extract the text value of the following entities:
{
\"name\": \"\",
\"address\": \"\",
\"registration_number\": \"\",
\"document_refrence_number\": \"\",
\"aquired_vehicle_on\": \"\",
\"no._of_former_keepers\": \"\",
}

- The JSON schema must be followed during the extraction.
- The values must only include text found in the document
- Do not normalize any entity value.
- If an entity is not found in the document, set the entity value to null.

    """,
    variables={},
)
