import json

def ollama_status(base_url="http://localhost:11434"):
    try:
        import urllib.request
        with urllib.request.urlopen(base_url.rstrip("/") + "/api/tags", timeout=2) as response:
            return {"available": response.status == 200, "base_url": base_url}
    except Exception as exc:
        return {"available": False, "base_url": base_url, "error": str(exc)}

def summarize_locally(evidence, *, model="qwen2.5:3b", client=None):
    if client is None:
        try:
            import ollama as client
        except ImportError:
            return {"available": False, "source": "deterministic_fallback",
                    "summary": "Local model unavailable; review structured evidence."}
    prompt = "Return JSON with summary, missing_information, recommended_next_step. Use only this evidence: " + json.dumps(evidence, sort_keys=True)
    try:
        response = client.chat(model=model, messages=[{"role": "user", "content": prompt}])
        content = response["message"]["content"] if isinstance(response, dict) else response.message.content
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("LLM response is not an object")
        return {"available": True, "source": "ollama", **parsed}
    except Exception as exc:
        return {"available": False, "source": "deterministic_fallback", "error": str(exc),
                "summary": "Local model response unavailable; review structured evidence."}
