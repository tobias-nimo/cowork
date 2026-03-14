# src/tools/groq.py

"""
Describe a local image file using Groq's vision model.
A system prompt loaded from a Markdown file instructs the model to produce
exhaustive descriptions so that someone who cannot see the image understands
it fully, while also answering an optional query about it.

Limits (Groq API):
  - Base64 requests  : max 4 MB
  - URL requests     : max 20 MB
  - Max resolution   : 33 megapixels per image
  - Max images/req   : 5
"""

import base64
from pathlib import Path

from groq import Groq
from langchain.tools import tool
from langchain_core.tools import ToolException

from ..config import settings
from ..prompts import prompts

# ── Constants ─────────────────────────────────────────────────────────────────

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".avif", ".tiff", ".tif",
                        ".gif", ".heic", ".heif", ".bmp", ".webp"}

IMAGE_MIME_TYPES: dict[str, str] = {
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png":  "image/png",
    ".avif": "image/avif",
    ".tiff": "image/tiff",
    ".tif":  "image/tiff",
    ".gif":  "image/gif",
    ".heic": "image/heic",
    ".heif": "image/heif",
    ".bmp":  "image/bmp",
    ".webp": "image/webp",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _encode_image(path: Path) -> str:
    """Return a base64 data-URI string for the given image file."""
    ext = path.suffix.lower()
    media_type = IMAGE_MIME_TYPES[ext]
    b64 = base64.standard_b64encode(path.read_bytes()).decode()
    return f"data:{media_type};base64,{b64}"


# ── Tool ──────────────────────────────────────────────────────────────────────

@tool
def describe_image(image_path: str, query: str = "") -> str:
    """
    Describe a local image in exhaustive detail using a VLM.
    Optionally answer a specific query about the image alongside the description.
    Returns the VLM's full text response.

    Args:
        image_path: Absolute or relative path to the image file.
        query: Optional question about the image. If empty, only the detailed description is returned.
    """
    try:
        path = Path(image_path).expanduser().resolve()

        if not path.exists():
            raise ToolException(f"Image not found: {path}")

        ext = path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ToolException(
                f"Unsupported image extension '{ext}'. "
                f"Supported: {sorted(SUPPORTED_EXTENSIONS)}"
            )

        system_prompt = prompts.get("vision")
        image_data_uri = _encode_image(path)

        # Build the user message — always include the image; append the query if given
        user_content = []

        user_text = "Please describe this image in full detail."
        if query.strip():
            user_text += f"\n\nAdditionally, answer the following question: {query.strip()}"
        user_content.append({"type": "text", "text": user_text})
        user_content.append({"type": "image_url", "image_url": {"url": image_data_uri}})

        client = Groq(api_key=settings.groq_api_key)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_content},
            ],
            max_completion_tokens=2048,
            temperature=0.2, # low temp -> factual, consistent descriptions
        )

        return response.choices[0].message.content

    except ToolException:
        raise
    except Exception as e:
        raise ToolException(f"describe_image failed: {e}")


describe_image.handle_tool_error = True