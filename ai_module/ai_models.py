import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import (
    GoogleSerperAPIWrapper,
    WikipediaAPIWrapper,
)
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents.agent_toolkits import NLAToolkit
from langchain.chains.llm_math.base import LLMMathChain
from langchain.memory import ConversationBufferMemory
#for image generation
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

#for Vision
import base64
from typing import Union, Optional
from google import genai
from google.genai import types
from ai_module.gcloud_services import setup_google_credentials

class TeacherChatAgent:
    def __init__(self, model="models/gemini-2.5-flash", temperature=0.2, max_tokens=2048):
        self._load_env()
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        self.search_tool = Tool(
            name="Search",
            func=GoogleSerperAPIWrapper().run,
            description="Useful for answering current events, recent data, or factual queries."
        )

        self.wiki_tool = Tool(
            name="Wikipedia",
            func=WikipediaAPIWrapper().run,
            description="Useful for getting background on academic topics."
        )

        self.math_chain = LLMMathChain.from_llm(self.llm, verbose=True)
        self.calc_tool = Tool(
            name="Calculator",
            func=self.math_chain.run,
            description="Useful for solving math and numeric problems."
        )

        self.ddg_search = Tool(
            name="DuckDuckGoSearch",
            func=DuckDuckGoSearchRun().run,
            description="Useful for searching the internet or educational videos."
        )
        def summarize_text(text: str) -> str:
            prompt = f"Summarize this for school teachers in simple language:\n\n{text}"
            return self.llm.predict(prompt)
        
        self.summarizer_tool = Tool(
            name="Summarizer",
            func=summarize_text,
            description="Summarizes long educational text into simple form for teachers or students."
        )

        def generate_story(topic: str) -> str:
            prompt = (
                f"Write a short, engaging story for school children in India based on this topic:\n\n{topic}\n"
                "Use age-appropriate language and include a moral at the end."
            )
            return self.llm.predict(prompt)
        
        # Story generator tool
        self.story_tool = Tool(
            name="Story Generator",
            func=generate_story,
            description="Generates short, moral-based stories on a topic for Indian school children."
        )
        self.system_prompt = (
            "Remember that Your Name is Sahayak, When User Asks about your name say Sahayak"
            "You are an AI assistant for Indian school teachers. "
            "when user wishes you, response with Hello I am Sahayak AI"
            "You provide curriculum-aligned, age-appropriate responses with Indian examples. "
            "Reply in the user's language when requested. Use tools to search the web, explain concepts, and solve problems. "
            "If asked for English word meanings, provide meanings in their native language. "
            "USE Tools Whenever Needed"
            "Dont give in local language until asked by user"
        )

        # Combine tools
        tools = [
            self.search_tool,
            self.wiki_tool,
            self.calc_tool,
            self.ddg_search,
            self.summarizer_tool,
            self.story_tool
        ]
        self.memory = ConversationBufferMemory(memory_key="memory", k=5, return_messages=False)  

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent="chat-conversational-react-description",
            verbose=True,
            # memory=self.memory,
            agent_kwargs={"system_message": self.system_prompt}
        )

    def _load_env(self):
        load_dotenv(".env", override=False)
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

    
    def chat(self, user_input: str, chat_history=None, history = None) -> str:
        """Process user input and return agent response."""
        if history is not None:
            prefix = f"remember the History {history}"
            user_input = prefix + user_input
        if chat_history is None:
            chat_history = []
        return self.agent.run({
            "input": user_input,
            "chat_history": chat_history
        })

    @staticmethod
    def format_history(messages: list[dict]) -> list[tuple[str, str]]:
        """Convert Streamlit-style message history into LangChain format."""
        return [("human" if m["role"] == "user" else "ai", m["content"]) for m in messages]


class ImageSceneGenerator:
    def __init__(
        self,
        project_id=None,
        location=None,
        model_name="imagen-4.0-generate-preview-06-06",
        number_of_images=4,
        aspect_ratio="1:1",
        safety_filter_level="block_few",
        add_watermark=False,
        person_generation="allow_all",
    ):
        load_dotenv()
        self.project_id = project_id or os.getenv("PROJECT_ID")
        self.location = location or os.getenv("LOCATION")

        if not self.project_id or not self.location:
            raise ValueError("PROJECT_ID and LOCATION must be set in .env or passed to the constructor.")

        vertexai.init(project=self.project_id, location=self.location)
        self.model = ImageGenerationModel.from_pretrained(model_name)

        self.default_settings = {
            "number_of_images": number_of_images,
            "aspect_ratio": aspect_ratio,
            "safety_filter_level": safety_filter_level,
            "add_watermark": add_watermark,
            "person_generation": person_generation,
        }

    def generate_images(
        self,
        prompt: str,
        number_of_images=None,
        aspect_ratio=None,
        safety_filter_level=None,
        person_generation=None,
        add_watermark=None,
        negative_prompt: str = "",
    ):
        settings = {
            "number_of_images": number_of_images or self.default_settings["number_of_images"],
            "aspect_ratio": aspect_ratio or self.default_settings["aspect_ratio"],
            "safety_filter_level": safety_filter_level or self.default_settings["safety_filter_level"],
            "person_generation": person_generation or self.default_settings["person_generation"],
            "add_watermark": add_watermark if add_watermark is not None else self.default_settings["add_watermark"],
        }

        print("Generating images with settings:", settings)

        return self.model.generate_images(
            prompt=prompt,
            negative_prompt=negative_prompt,
            **settings
        )
    

class GeminiVisionQA:
    def __init__(self, location: str = "global", model: str = "gemini-2.5-flash-lite"):
        setup_google_credentials()
        self.project_id = os.getenv('VISION_PROJECT_ID')
        self.client = genai.Client(vertexai=True, project=self.project_id, location=location)
        self.model = model

    def _prepare_image_part(self, image: Union[str, bytes], mime_type: str = "image/jpeg") -> types.Part:
        """
        Accepts GS URI, local path, or raw bytes. Returns correct types.Part.
        """
        if isinstance(image, str):
            if image.startswith("gs://"):
                return types.Part.from_uri(file_uri=image, mime_type=mime_type)
            elif os.path.exists(image):
                with open(image, "rb") as f:
                    data = f.read()
                return types.Part.from_bytes(data=data, mime_type=mime_type)
        elif isinstance(image, (bytes, bytearray)):
            return types.Part.from_bytes(data=image, mime_type=mime_type)

        raise ValueError("Image must be GCS URI, file path, or bytes.")

    def ask_about_image(self, image: Union[str, bytes], prompt_text: str) -> str:
        """
        Sends the visual + text prompt to Gemini Vision and returns the response.
        """
        image_part = self._prepare_image_part(image)
        text_part = types.Part.from_text(text=prompt_text)

        contents = types.Content(
            role="user",
            parts=[image_part, text_part]
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[contents],
            config=types.GenerateContentConfig()
        )

        # The response text is available via response.text or first candidate
        return getattr(response, "text", "").strip()

class GeminiVisionQAWeb:
    def __init__(
        self,
        project_id: str,
        location: str = "global",
        model: str = "gemini-2.5-flash-lite",
        serp_api_key: Optional[str] = os.getenv("SERPER_API_KEY")
    ):
        setup_google_credentials()
        self.client = genai.Client(vertexai=True, project=project_id, location=location)
        self.model = model
        self.web_search_client = GoogleSerperAPIWrapper(serpapi_api_key=serp_api_key) if serp_api_key else None

    def _load_env(self):
        load_dotenv(".env", override=False)
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        self.serp_api_key = os.getenv("SERPER_API_KEY")

    def _prepare_image_part(self, image: Union[str, bytes], mime_type: str = "image/jpeg") -> types.Part:
        if isinstance(image, str):
            if image.startswith("gs://"):
                return types.Part.from_uri(file_uri=image, mime_type=mime_type)
            elif os.path.exists(image):
                with open(image, "rb") as f:
                    data = f.read()
                return types.Part.from_bytes(data=data, mime_type=mime_type)
        elif isinstance(image, (bytes, bytearray)):
            return types.Part.from_bytes(data=image, mime_type=mime_type)
        raise ValueError("Image must be GCS URI, file path, or bytes.")

    def _web_search(self, query: str) -> Optional[str]:
        if not self.web_search_client:
            return None
        try:
            results = self.web_search_client.run(query)
            return results.strip()
        except Exception as e:
            print(f"Web search error: {e}")
            return None

    def _generate_image_caption(self, image_part: types.Part) -> str:
        caption_prompt = "Describe the main objects and scene in this image in a concise way."
        contents = types.Content(
            role="user",
            parts=[image_part, types.Part.from_text(text=caption_prompt)]
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=[contents],
            config=types.GenerateContentConfig()
        )
        return getattr(response, "text", "").strip()


    def ask_about_image(self, image: Union[str, bytes], prompt_text: str, use_web_search: bool = False) -> str:
        image_part = self._prepare_image_part(image)

        # Step 1: Get image caption
        image_caption = self._generate_image_caption(image_part)

        # Step 2: Combine image caption + user question for web search context
        enriched_prompt = f"Image Description: {image_caption}; Question: {prompt_text}"

        if use_web_search and self.web_search_client:
            print("Performing web search for additional context...")
            web_results = self._web_search(enriched_prompt)
            if web_results:
                enriched_prompt = (
                    f"Image Description: {image_caption} and Web search results:{web_results} and Answer the question based on the image and web info: {prompt_text}"
                )
        else:
            enriched_prompt = f"Image Description is {image_caption} and Question: {prompt_text}"
        # print(f"Enriched Prompt: {enriched_prompt}")
        # Step 3: Query Gemini Vision with image + enriched prompt
        final_text_part = types.Part.from_text(text=str(enriched_prompt))
        contents = types.Content(
            role="user",
            parts=[image_part, final_text_part]
        )

        final_response = self.client.models.generate_content(
            model=self.model,
            contents=[contents],
            config=types.GenerateContentConfig()
        )

        return getattr(final_response, "text", "").strip()


    
def save_chat_history(messages):
    history = []
    for msg in messages:
        role = "human" if msg["role"] == "user" else "ai"
        history.append((role, msg["content"]))
    return history
