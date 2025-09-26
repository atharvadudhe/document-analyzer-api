import asyncio
from typing import Dict, List
import re

# Transformers and spaCy will be loaded lazily to avoid startup cost
from transformers import pipeline
import spacy

# Keep globals for loaded models to reuse between requests
_transformer_summarizer = None
_spacy_nlp = None

async def _load_summarizer():
    global _transformer_summarizer
    if _transformer_summarizer is None:
        # Initialize a summarization pipeline (hugsface model). This may download weights on first run.
        # We wrap in asyncio.to_thread because initialization is blocking/IO heavy.
        def _init():
            return pipeline('summarization')
        _transformer_summarizer = await asyncio.to_thread(_init)
    return _transformer_summarizer

async def _load_spacy():
    global _spacy_nlp
    if _spacy_nlp is None:
        # Load small English model. Ensure the spaCy model is installed separately.
        def _init():
            return spacy.load('en_core_web_sm')
        _spacy_nlp = await asyncio.to_thread(_init)
    return _spacy_nlp

async def summarize_text(text: str, max_length: int = 120) -> str:
    summarizer = await _load_summarizer()
    input_text = text.strip()
    if len(input_text) < 30:
        return input_text
    def _summarize(t: str):
        return summarizer(t, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']

    try:
        return await asyncio.to_thread(_summarize, input_text)
    except Exception:
        return input_text.split('\n')[0][:max_length]

async def extract_entities(text: str) -> List[Dict]:
    """Extract named entities using spaCy and return list of {text, label} dicts."""
    nlp = await _load_spacy()

    def _ent(t: str):
        doc = nlp(t)
        return [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]

    return await asyncio.to_thread(_ent, text)

async def extract_keywords(text: str, top_k: int = 10) -> List[str]:
    """Simple frequency-based keyword extraction using spaCy tokenization and stopwords.
    This is intentionally basic; replace with TF-IDF for a more robust approach.
    """
    nlp = await _load_spacy()

    def _keywords(t: str):
        doc = nlp(t.lower())
        candidates = [token.lemma_ for token in doc
                      if token.is_alpha and not token.is_stop and token.pos_ in ('NOUN', 'PROPN', 'ADJ')]
        if not candidates:
            return []
        freq = {}
        for c in candidates:
            freq[c] = freq.get(c, 0) + 1
        sorted_items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [item[0] for item in sorted_items[:top_k]]

    return await asyncio.to_thread(_keywords, text)

async def analyze_text(text: str) -> Dict:
    summary_task = asyncio.create_task(summarize_text(text))
    entities_task = asyncio.create_task(extract_entities(text))
    keywords_task = asyncio.create_task(extract_keywords(text))

    summary = await summary_task
    entities = await entities_task
    keywords = await keywords_task

    return {
        'summary': summary,
        'entities': entities,
        'keywords': keywords,
    }