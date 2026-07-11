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

MERGE (maria:Person {id: "dev-person-maria"})
SET
    maria.name = "Maria Skłodowska-Curie",
    maria.email = "maria@example.local",
    maria.note = "Example development person",
    maria.updated_at = datetime(),
    maria.created_at = coalesce(maria.created_at, datetime());

MERGE (jan:Person {id: "dev-person-jan"})
SET
    jan.name = "Jan Kowalski",
    jan.email = "jan@example.local",
    jan.note = "Example development person",
    jan.updated_at = datetime(),
    jan.created_at = coalesce(jan.created_at, datetime());

MERGE (warsaw:City {id: "dev-city-warsaw"})
SET
    warsaw.name = "Warszawa",
    warsaw.country = "Polska",
    warsaw.note = "Example development city",
    warsaw.updated_at = datetime(),
    warsaw.created_at = coalesce(warsaw.created_at, datetime());

MERGE (krakow:City {id: "dev-city-krakow"})
SET
    krakow.name = "Kraków",
    krakow.country = "Polska",
    krakow.note = "Example development city",
    krakow.updated_at = datetime(),
    krakow.created_at = coalesce(krakow.created_at, datetime());

MERGE (gdansk:City {id: "dev-city-gdansk"})
SET
    gdansk.name = "Gdańsk",
    gdansk.country = "Polska",
    gdansk.note = "Example development city",
    gdansk.updated_at = datetime(),
    gdansk.created_at = coalesce(gdansk.created_at, datetime());

MATCH (ada:Person {id: "dev-person-ada"})
MATCH (warsaw:City {id: "dev-city-warsaw"})
MERGE (ada)-[ada_warsaw:MIESZKA_W]->(warsaw)
ON CREATE SET ada_warsaw.created_at = datetime()
SET ada_warsaw.updated_at = datetime();

MATCH (grace:Person {id: "dev-person-grace"})
MATCH (krakow:City {id: "dev-city-krakow"})
MERGE (grace)-[grace_krakow:MIESZKA_W]->(krakow)
ON CREATE SET grace_krakow.created_at = datetime()
SET grace_krakow.updated_at = datetime();

MATCH (maria:Person {id: "dev-person-maria"})
MATCH (warsaw:City {id: "dev-city-warsaw"})
MERGE (maria)-[maria_warsaw:MIESZKA_W]->(warsaw)
ON CREATE SET maria_warsaw.created_at = datetime()
SET maria_warsaw.updated_at = datetime();

MATCH (jan:Person {id: "dev-person-jan"})
MATCH (gdansk:City {id: "dev-city-gdansk"})
MERGE (jan)-[jan_gdansk:MIESZKA_W]->(gdansk)
ON CREATE SET jan_gdansk.created_at = datetime()
SET jan_gdansk.updated_at = datetime();

RETURN "seed_dev completed" AS status;
