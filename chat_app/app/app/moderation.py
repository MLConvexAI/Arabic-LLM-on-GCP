from google.cloud import language
from google.cloud import translate_v2 as translate

# detects if the language is Arabic or English
def detect_language(text: str) -> str:

    translate_client = translate.Client()
    result = translate_client.detect_language(text)

    language = "NA"
    if result["confidence"] > 0.7:
        if result["language"] == 'ar' or result["language"] == 'en':
            language = result["language"]

    return language


# check the prediction quality
def moderate_text(text: str) -> language.ModerateTextResponse:

    client = language.LanguageServiceClient()
    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
    )
    return client.moderate_text(document=document)


# verifies if the prediction contains inapproriate content above threshold defined in responses
def text_appropriate(responses: language.ModerateTextResponse, threshold: float = 0.8) -> bool:
  
    for category in responses.moderation_categories:
        if category.confidence > threshold:
            return False
    return True