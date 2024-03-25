import requests
from core.common.const import LLMConfig, console


def download_nitro():
    # download nitro based on operating system
    pass


def check_nitro_health() -> bool:
    url = f"{LLMConfig.NITRO_SERVER_URL}/healthz"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False


def load_model_into_nitro(model_path) -> bool:
    with console.status("[cyan]Loading model into Nitro...", spinner="monkey"):
        url = f"{LLMConfig.NITRO_SERVER_URL}/inferences/llamacpp/loadmodel"
        headers = {"Content-Type": "application/json"}
        data = {"llama_model_path": model_path, "ctx_len": 512, "ngl": 100}

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.json()["message"] == "Model already loaded":
                return True

            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False
