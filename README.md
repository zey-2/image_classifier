# image_classifier

## Usage

1. Create a Telegram bot via BotFather and copy the bot token.
2. Set the token in environment variable `TELEGRAM_API_KEY`:

```bash
export TELEGRAM_API_KEY="<your-telegram-bot-token>"
```

3. Run the bot:

```bash
python app.py
```

The bot will print a message when it starts and listen for image messages submitted to the Telegram bot.

## Docker

You can run this bot inside a Docker container instead of running it directly on your host. The Docker image uses `requirements.txt` to install dependencies in the container.

1. Build the Docker image (run from project root):

```bash
docker build -t image_classifier:latest .
```

2. Run the container with your Telegram bot token:

```bash
docker run --rm -e TELEGRAM_API_KEY="<your-telegram-bot-token>" image_classifier:latest
```

Notes:

- The model weights will be downloaded from Hugging Face the first time the container starts. This may take extra time and network bandwidth.
- You may mount a local cache to speed things up on repeated runs, for example on Linux/macOS (bash):

```bash
docker run --rm -e TELEGRAM_API_KEY="<your-telegram-bot-token>" -v $HOME/.cache/huggingface:/root/.cache/huggingface image_classifier:latest
```

- This Dockerfile is designed for CPU-only operation. If you have a GPU and want to use CUDA-accelerated PyTorch, use an appropriate CUDA-enabled base image and install the matching `torch` package (not covered here).

## Deployment note

Cloud Run deploy instructions have been removed: this bot uses Telegram long-polling and does not start an HTTP server that listens on the `PORT` environment variable Cloud Run requires. Deploying to Cloud Run as-is will fail unless you convert the bot to webhook mode or add an HTTP server that listens on `PORT` and responds to readiness checks.

Alternatives:

- Convert to webhook mode so Cloud Run can receive incoming HTTP requests via the `PORT` variable (recommended for serverless).
- Use a VM or Kubernetes/ GKE for long-running processes (polling) if you prefer not to change the bot to webhooks.
