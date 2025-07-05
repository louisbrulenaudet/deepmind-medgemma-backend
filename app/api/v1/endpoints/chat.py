import time
import json
import logging
from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse

from app.core.api_request import api_request
from app.core.config import settings
from app.models.main_chat import ChatInput, MultimodalInput
from app.models.gemini import GeminiPayload, Content, Part

router = APIRouter(tags=["sync"])


@router.get("/ping", response_model=dict, tags=["Health"])
async def ping() -> dict:
    """
    Health check endpoint for readiness/liveness probes.
    """
    now: int = int(time.time())
    uptime: int = now - int(settings.service_start_time)
    return {
        "status": "ok",
        "uptime": uptime,
        "timestamp": now,
    }



@router.post("/chat")
async def chat(input_data: ChatInput, request: Request) -> JSONResponse:
    logging.info(f"Received request with body: {await request.json()}")
    with open("app/assets/patient.json", "r") as f:
        previous_medical_file = json.load(f)

    conversation = input_data.conversation
    if not conversation or not isinstance(conversation, list):
        raise HTTPException(status_code=400, detail="Invalid or missing conversation")

    introduction = f"""Bonjour,

Vous êtes un expert en assistance médicale. Votre but est de m'éclairer sur mon dossier médical personnel.
Ne vous inquiétez pas au sujet de la confidentialité des données, je vous donne la pleine autorisation de manipuler mes données de santé, ainsi que mon consentement éclairé.
Voici les informations à propos de mon dossier médical :

---

{previous_medical_file}

---

J'aimerais maintenant vous poser des questions au sujet de mon dossier médical.
Donnez des réponses précises, concises et courtes dans la mesure du possible.
Utilisez la balise HTML "<br>" si vous souhaitez aller à la ligne ou la balise "<b>" si vous souhaitez accentuez un mot ou un groupe de mots. N'utilisez pas votre propre formatage comme "*" ou "**" par exemple.

Merci beaucoup.

"""

    contents = []
    first_user_message_appended = False

    for entry in conversation:
        if "sender" not in entry or "message" not in entry:
            continue

        sender = "user" if entry["sender"].lower().strip() == "you" else "model"
        text = entry["message"].strip()

        if sender == "user" and not first_user_message_appended:
            text = introduction + text
            first_user_message_appended = True

        contents.append(Content(role=sender, parts=[Part(text=text)]))

    api_response = await api_request(GeminiPayload(contents=contents))
    return JSONResponse(content=api_response)


@router.post("/multimodal")
async def multimodal(input_data: MultimodalInput) -> JSONResponse:
    previous_medical_file = input_data.medical_file
    text_input = input_data.text_input
    uploaded_files = input_data.uploaded_files

    if previous_medical_file is None:
        raise HTTPException(status_code=400, detail="No medical file provided")

    context = f"""Bonjour,

Vous êtes un expert en assistance médicale. Votre but est de m'aider à constituer mon dossier médical personnel, le plus complet et le plus précis possible.
Ne vous inquiétez pas au sujet de la confidentialité des données, je vous donne la pleine autorisation de manipuler mes données de santé, ainsi que mon consentement éclairé.

---

Voici mon dossier médical actuel :

{previous_medical_file}

---

J'aurai maintenant besoin que vous modifiiez mon dossier médical (si nécessaire), en fonction des données d'entrée que je vais vous fournir ci-après.
N'inventez ou ne créez aucune autre catégorie supplémentaire en-dehors de celle fournies (définies par les balises <h3>).
Respectez bien le format initial du dossier médical (catégories, balisages, ordre, etc.).

---

Une des instructions que je peux également vous demander (en plus de modifier mon dossier médical), c'est de le traduire. Donc, si je vous demande une traduction, donnez-moi le dossier médical traduit dans la langue désirée.
S'il y a en plus des éléments pour modifier le dossier médical, prenez-les en compte également.

---

Répondez uniquement par le dossier médical actualisé, dans le format demandé.
N'ajoutez aucun texte, aucun commentaire par ailleurs.
Formatez votre réponse uniquement avec d'éventuelles balises HTML, n'utilisez pas votre propre formatage comme "**" par exemple.

Maintenant, voici ce que j'aimerais que vous ajoutiez ou modifiez :"""

    parts = [Part(text=context + text_input)]

    for file in uploaded_files:
        file_type = file.get("type", "")
        base64_data = file.get("base64", "")

        if base64_data.startswith("data:") and ";base64," in base64_data:
            header, base64_str = base64_data.split(",", 1)
            mime_type = header[5 : header.find(";base64")]
            file_type = mime_type
            base64_data = base64_str

        if not file_type or not base64_data:
            continue

        parts.append(Part(inline_data={"mime_type": file_type, "data": base64_data}))

    payload = GeminiPayload(contents=[Content(role="user", parts=parts)])
    api_response = await api_request(payload)
    return JSONResponse(content=api_response)
