# !pip install python-telegram-bot==20.7 transformers torch pillow

# Fix Runtime Error: Cannot close a running event loop
import nest_asyncio
nest_asyncio.apply()

import logging
import torch
from PIL import Image
from io import BytesIO
from transformers import AutoImageProcessor, ViTForImageClassification
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# -------------------------------------
# Load Model (Vision Transformer)
# -------------------------------------
model_name = "google/vit-base-patch16-224"
image_processor = AutoImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)

# -------------------------------------
# Logging (optional)
# -------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# -------------------------------------
# Start Command
# -------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me an image and I will classify it using ViT.")

# -------------------------------------
# Image Handler
# -------------------------------------
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # highest resolution
    file = await photo.get_file()
    image_bytes = await file.download_as_bytearray()

    # Convert bytes → PIL image
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Preprocess
    inputs = image_processor(images=img, return_tensors="pt")

    # Run model
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_idx = logits.argmax(-1).item()
    predicted_label = model.config.id2label[predicted_idx]

    await update.message.reply_text(f"Prediction: **{predicted_label}**")

# -------------------------------------
# Main function
# -------------------------------------
import os


def get_bot_token():
    """Return the Telegram bot token.

    Checks the `TELEGRAM_API_KEY` environment variable first. If not set, tries
    to load from Google Colab `userdata` (backwards compatibility). Raises
    RuntimeError if none found.
    """
    # Check the canonical environment variable
    token = os.getenv("TELEGRAM_API_KEY")
    # Backwards compatibility: sometimes called BOT_TOKEN or TELEGRAM_BOT_TOKEN
    if not token:
        token = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        return token

    try:
        # In Google Colab you can store user settings. Keep backwards-compatibility.
        from google.colab import userdata

        token = userdata.get('TELEGRAM_API_KEY')
        if token:
            return token
    except Exception:
        # Google Colab not available; ignore
        pass

    raise RuntimeError(
        "TELEGRAM_API_KEY not set. Export it with `export TELEGRAM_API_KEY=...`. "
        "(Alternatively set BOT_TOKEN or TELEGRAM_BOT_TOKEN.)"
    )


async def main():
    BOT_TOKEN = get_bot_token()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("🤖 Bot running… Send an image to your bot!")
    await app.run_polling()

# Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
