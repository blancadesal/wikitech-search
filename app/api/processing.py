import logging
import pickle

import mwparserfromhell
import requests
from annoy import AnnoyIndex
from mwedittypes.utils import wikitext_to_plaintext
from sentence_transformers import SentenceTransformer
from transformers import pipeline

from app.config import settings

log = logging.getLogger("uvicorn")

EMB_DIR = settings.emb_dir

emb_model_name = "sentence-transformers/all-mpnet-base-v2"
EMB_MODEL = SentenceTransformer(emb_model_name, cache_folder=EMB_DIR)
ANNOY_INDEX = AnnoyIndex(768, "angular")
IDX_TO_SECTION = []

qa_model_name = "deepset/tinyroberta-squad2"
QA_MODEL = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)


def get_model_info():
    return {"q&a": qa_model_name, "emb": emb_model_name}


def get_answer(query, context):
    """Run Q&A model to extract best answer to query."""
    qa_input = {
        "question": query,
        "context": "\n".join(context),  # maybe reverse inputs?
    }
    try:
        res = QA_MODEL(qa_input)
        return res["answer"]
    except Exception:
        return None


def get_inputs(query, result_depth=3):
    """Build inputs to Q&A model for query."""
    embedding = EMB_MODEL.encode(query)
    nns = ANNOY_INDEX.get_nns_by_vector(
        embedding, result_depth, search_k=-1, include_distances=True
    )
    results = []
    for i in range(result_depth):
        idx = nns[0][i]
        score = 1 - nns[1][i]
        title = IDX_TO_SECTION[idx]
        try:
            wt = _get_wikitext(title)
            pt = _get_section_plaintext(title, wt).strip()
            results.append({"title": title, "score": score, "text": pt})
        except Exception:
            continue

    return results


def _get_wikitext(title, domain="wikitech.wikimedia"):
    """Get wikitext for an article."""
    try:
        base_url = f"https://{domain}.org/w/api.php"
        params = {
            "action": "query",
            "prop": "revisions",
            "titles": title.split("#", maxsplit=1)[0],
            "rvslots": "*",
            "rvprop": "content",
            "rvdir": "older",
            "rvlimit": 1,
            "format": "json",
            "formatversion": 2,
        }
        r = requests.get(
            url=base_url, params=params, headers={"User-Agent": settings.custom_ua}
        )
        rj = r.json()
        return rj["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
    except Exception:
        return None


def _get_section_plaintext(title, wikitext):
    """Convert section wikitext into plaintext.

    This does a few things:
    * Excludes certain types of nodes -- e.g., references, templates.
    * Strips wikitext syntax -- e.g., all the brackets etc.
    ."""
    try:
        section = title.split("#", maxsplit=1)[1]
        for s in mwparserfromhell.parse(wikitext).get_sections(flat=True):
            try:
                header = s.filter_headings()[0].title.strip().replace(" ", "_")
                if header == section:
                    return wikitext_to_plaintext(s)
            except Exception:
                continue
    except Exception:
        # default to first section if no section in title
        return wikitext_to_plaintext(
            mwparserfromhell.parse(wikitext).get_sections(flat=True)[0]
        )


async def load_similarity_index():
    """Load in nearest neighbor index and labels."""
    global IDX_TO_SECTION
    index_fp = EMB_DIR / "embeddings.ann"
    labels_fp = EMB_DIR / "section_to_idx.pickle"
    log.info("Using pre-built ANNOY index")
    ANNOY_INDEX.load(str(index_fp))
    with open(labels_fp, "rb") as fin:
        IDX_TO_SECTION = pickle.load(fin)
    log.info(f"{len(IDX_TO_SECTION)} passages in nearest neighbor index.")
