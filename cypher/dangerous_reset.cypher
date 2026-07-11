// DANGEROUS RESET TEMPLATE
//
// This file intentionally contains no executable destructive statement.
// Do not run a database reset unless the user explicitly asks for it and confirms
// the target database. Prefer backups before any destructive operation.
//
// If a reset is explicitly approved, write the command manually in the Neo4j
// Browser or a controlled migration script after confirming the environment.
//
// Example of what must NOT be run casually:
// MATCH (n)
// DETACH DELETE n;
