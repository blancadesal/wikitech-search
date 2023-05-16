import logging
import pickle

import mwparserfromhell
from annoy import AnnoyIndex
from mwedittypes.utils import wikitext_to_plaintext
from sentence_transformers import SentenceTransformer
from transformers import pipeline

from app.config import settings
from app.wiki_api import WikiAPI

log = logging.getLogger("uvicorn")


class ModelManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, emb_model_name="sentence-transformers/all-mpnet-base-v2", qa_model_name="deepset/tinyroberta-squad2", emb_dir=settings.emb_dir):
        if not hasattr(self, 'initialized'):
            self.emb_dir = emb_dir
            self.emb_model_name = emb_model_name
            self.qa_model_name = qa_model_name
            self.EMB_MODEL = SentenceTransformer(self.emb_model_name)
            self.QA_MODEL = pipeline("question-answering", model=self.qa_model_name, tokenizer=self.qa_model_name)
            self.ANNOY_INDEX = AnnoyIndex(768, "angular")
            self.IDX_TO_SECTION = []
            self.wiki_api = WikiAPI()
            self.initialized = True

    def load_similarity_index(self):
        """Load in nearest neighbor index and labels."""
        index_fp = self.emb_dir / "msmarco-distilbert-base-v4_embeddings.ann"
        labels_fp = self.emb_dir / "msmarco-distilbert-base-v4_section-to-idx.pickle"
        log.info("Using pre-built ANNOY index")
        self.ANNOY_INDEX.load(str(index_fp))
        with open(labels_fp, "rb") as fin:
            self.IDX_TO_SECTION = pickle.load(fin)
        log.info(f"{len(self.IDX_TO_SECTION)} passages in nearest neighbor index.")

    def get_model_info(self):
        return {"q&a": self.qa_model_name, "emb": self.emb_model_name}

    def get_answer(self, query, context):
        """Run Q&A model to extract best answer to query."""
        qa_input = {
            "question": query,
            "context": "\n".join(context),  # maybe reverse inputs?
        }
        try:
            res = self.QA_MODEL(qa_input)
            return res["answer"]
        except Exception:
            return None

    def get_inputs(self, query, result_depth=3):
        """Build inputs to Q&A model for query."""
        embedding = self.EMB_MODEL.encode(query)
        nns = self.ANNOY_INDEX.get_nns_by_vector(
            embedding, result_depth, search_k=-1, include_distances=True
        )
        results = []
        for i in range(result_depth):
            idx = nns[0][i]
            score = 1 - nns[1][i]
            title = self.IDX_TO_SECTION[idx]
            try:
                wt = self.wiki_api.get_wikitext(title)
                pt = self._get_section_plaintext(title, wt).strip()
                results.append({"title": title, "score": score, "text": pt})
            except Exception as e:
                log.info(f'Exception: {e}')
                continue
        return results

    @staticmethod
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


def get_model_manager():
    return ModelManager()
