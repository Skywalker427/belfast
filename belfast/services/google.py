import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from google.oauth2 import service_account
from pydantic import BaseModel
from .secrets import get_secret


class Prompt(BaseModel):
    project_id: str
    content: str
    model_id: str
    temperature: float | None = None
    max_output_tokens: int | None = None
    top_p: float | None = None
    top_k: int | None = None
    location: str = "us-central1"
    tuned_model_name: str | None = None
    variables: dict | None = None

    def set_variables(self, **kwargs) -> None:
        """
        Sets the variables to be used in the prompt
        Args:
            **kwargs: variables to insert into the prompt
        """
        self.variables = {}
        for key, value in kwargs.items():
            self.variables[key] = value

    def authenticate(self):
        credentials_file = "/tmp/credentials.json"
        credentials_content = get_secret("/development/llm-prompt-middleware/google")
        with open(credentials_file, "w") as f:
            f.write(credentials_content)
            f.close()

        credentials = service_account.Credentials.from_service_account_file(credentials_file)
        vertexai.init(project=self.project_id, location=self.location, credentials=credentials)

    def call(self, image):
        """
        Prompts the model with the given content and returns the response

        Returns:
            str: The response from the model
        """
        content = self.content
        if self.variables:
            content = content.format(**self.variables)

        self.authenticate()

        model = GenerativeModel(self.model_id)

        image_part = Part.from_data(
            mime_type="image/jpeg",
            data=image,
        )

        responses = model.generate_content(
            [content, image_part],
            generation_config=self.model_dump(
                by_alias=True,
                exclude_none=True,
                include={"temperature", "max_output_tokens", "top_p", "top_k"},
            ),
        )

        return responses
