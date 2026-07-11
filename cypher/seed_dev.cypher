// Optional local development seed.
// This file is non-destructive and uses MERGE on stable example ids.

MERGE (ada:Person {id: "dev-person-ada"})
SET
    ada.name = "Ada Lovelace",
    ada.email = "ada@example.local",
    ada.note = "Example development person",
    ada.updated_at = datetime(),
    ada.created_at = coalesce(ada.created_at, datetime());

MERGE (grace:Person {id: "dev-person-grace"})
SET
    grace.name = "Grace Hopper",
    grace.email = "grace@example.local",
    grace.note = "Example development person",
    grace.updated_at = datetime(),
    grace.created_at = coalesce(grace.created_at, datetime());

RETURN "seed_dev completed" AS status;
