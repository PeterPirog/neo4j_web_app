from unittest import TestCase

from app.modules.relations import queries


class RelationshipQueryTests(TestCase):
    def test_allowed_relationship_type_is_substituted_after_validation(self) -> None:
        query = queries.create_relationship_query("WORKS_WITH")

        self.assertIn("[r:WORKS_WITH]", query)
        self.assertNotIn("RELATIONSHIP_TYPE", query)
        self.assertIn("$source_person_id", query)
        self.assertIn("$target_person_id", query)

    def test_disallowed_relationship_type_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            queries.create_relationship_query("MATCH (n) RETURN n")
