# USAGE

```sh
.venv/bin/python -c "
from api_clients import OllamaClient
from prompt_refiner import PromptRefiner
refiner = PromptRefiner(OllamaClient('gemma4:12b'))
print(refiner.refine_prompt(
    '1) What plants suit full sun in Brisbane? 2) How often should I water them?',
    'um maybe natives? idk, something hardy. watering like whenever it looks dry i guess'))"
```

Real output (23/08/2026, local Ollama):

```
1) I am looking for hardy native plants that can thrive in full sun.
2) They should be watered whenever the soil feels dry.
```

Full UI: `streamlit run app.py` — paste questions left, brain-dump middle, copy result right.
