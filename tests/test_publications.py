"""Regression cases for ORCID's mixed publisher/preprint records."""

import copy
import json
import unittest
from unittest.mock import patch

from scripts import update_publications as importer


def work(code=1, doi="", venue="", work_type="journal-article", url="", year=2024):
    return {
        "put-code": code,
        "title": {"title": {"value": "Example paper"}},
        "type": work_type,
        "journal-title": {"value": venue},
        "url": {"value": url},
        "publication-date": {"year": {"value": str(year)}},
        "external-ids": {"external-id": [identifier(doi)] if doi else []},
    }


def identifier(value, relationship="self", kind="doi"):
    return {
        "external-id-type": kind,
        "external-id-value": value,
        "external-id-relationship": relationship,
    }


class PublicationTests(unittest.TestCase):
    def test_published_regression_paper_beats_older_scopus_preprint(self):
        published = work(188489134, "10.1007/s10618-024-01027-w", "Data Mining and Knowledge Discovery")
        preprint = work(191191863, "10.48550/arXiv.2305.01429", "Arxiv", "other", "https://www.scopus.com/record", 2023)
        group = {"summaries": [preprint, published]}
        with patch.object(importer, "fetch_work", side_effect=lambda _, code, __: {188489134: published, 191191863: preprint}[code]):
            actual = importer.normalise_work(importer.fetch_best_group_work("id", group, "token"))
        self.assertEqual(actual["year"], 2024)
        self.assertEqual(actual["type"], "Journal article")
        self.assertEqual(actual["doi"], "10.1007/s10618-024-01027-w")
        self.assertEqual(importer.get_group_preprint_url(group), "https://arxiv.org/abs/2305.01429")

    def test_multiple_self_dois_prefer_publisher_in_either_order(self):
        record = work(171026654, venue="Data Mining and Knowledge Discovery")
        ids = [identifier("10.1007/s10618-024-01027-w"), identifier("10.48550/arXiv.2305.01429")]
        for order in (ids, list(reversed(ids))):
            with self.subTest(order=order):
                record["external-ids"]["external-id"] = order
                actual = importer.normalise_work(record)
                self.assertEqual(actual["doi"], "10.1007/s10618-024-01027-w")
                self.assertEqual(actual["preprint_url"], "https://arxiv.org/abs/2305.01429")

    def test_jmlr_record_with_only_arxiv_doi_keeps_journal_identity(self):
        record = work(171025653, "10.48550/arXiv.2406.14231", "Journal of Machine Learning Research", url="https://www.jmlr.org/papers/v25/23-1444.html")
        actual = importer.normalise_work(record)
        self.assertEqual(actual["type"], "Journal article")
        self.assertEqual(actual["doi"], "")
        self.assertEqual(actual["url"], "https://www.jmlr.org/papers/v25/23-1444.html")
        self.assertEqual(actual["preprint_url"], "https://arxiv.org/abs/2406.14231")

    def test_jmlr_without_doi_beats_arxiv_record(self):
        journal = work(1, venue="Journal of Machine Learning Research")
        journal["external-ids"]["external-id"] = [identifier("2406.14231", kind="arxiv")]
        preprint = work(2, "10.48550/arxiv.2406.14231", "Arxiv", "other")
        self.assertGreater(importer.work_quality_score(journal), importer.work_quality_score(preprint))
        self.assertEqual(importer.normalise_work(journal)["type"], "Journal article")

    def test_related_dois_do_not_replace_the_work_doi(self):
        record = work(doi="10.1007/chapter", venue="Proceedings", work_type="conference-paper")
        record["external-ids"]["external-id"] += [identifier("10.1007/book", "part-of"), identifier("10.48550/arxiv.1234.5678", "version-of")]
        actual = importer.normalise_work(record)
        self.assertEqual(actual["doi"], "10.1007/chapter")
        self.assertEqual(actual["preprint_url"], "https://arxiv.org/abs/1234.5678")

    def test_preprint_only_record_is_labelled_and_skips_crossref(self):
        actual = importer.normalise_work(work(doi="10.48550/arxiv.2603.20352", venue="Arxiv", work_type="other", url="https://www.scopus.com/record"))
        self.assertEqual(actual["type"], "Preprint")
        self.assertEqual(actual["url"], "https://arxiv.org/abs/2603.20352")
        with patch.object(importer, "fetch_crossref_metadata") as fetch:
            importer.enrich_with_crossref(actual)
        fetch.assert_not_called()

    def test_canonical_url_override_wins(self):
        actual = importer.normalise_work(work(doi="10.1007/example", url="https://www.scopus.com/record"))
        overrides = importer.load_overrides()
        overrides["url_overrides"]["doi:10.1007/example"] = "https://publisher.example/article"
        actual = importer.apply_overrides(actual, overrides, False)
        self.assertEqual(actual["url"], "https://publisher.example/article")

    def test_additions_survive_updates_and_do_not_duplicate_orcid(self):
        additions = json.loads(importer.ADDITIONS_PATH.read_text(encoding="utf-8"))
        imported = copy.deepcopy(additions)
        imported[0]["source"] = "ORCID"
        result = importer.merge_publication_additions(imported, importer.load_overrides())
        self.assertEqual(len(result), len(additions))
        self.assertEqual(result[0]["source"], "ORCID")
        self.assertEqual(len(importer.merge_publication_additions([], importer.load_overrides())), len(additions))

    def test_published_version_supersedes_curated_preprint_by_title(self):
        additions = json.loads(importer.ADDITIONS_PATH.read_text(encoding="utf-8"))
        published = copy.deepcopy(next(p for p in additions if p["type"] == "Preprint"))
        published.update(doi="10.1007/new-publication", type="Journal article", source="ORCID")
        result = importer.merge_publication_additions([published], importer.load_overrides())
        matches = [p for p in result if p["title"] == published["title"]]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["type"], "Journal article")


if __name__ == "__main__":
    unittest.main()
