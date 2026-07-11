from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.db import neo4j_connection, neo4j_lifespan
from app.people_service import (
    create_person,
    delete_person,
    ensure_constraints,
    get_person,
    list_people,
    update_person,
)

templates = Jinja2Templates(directory="app/templates")


app = FastAPI(lifespan=neo4j_lifespan)


def neo4j_error_message(exc: Exception | None = None) -> str:
    if exc is None:
        return "Nie można połączyć się z Neo4j. Sprawdź, czy baza działa i czy dane w .env są poprawne."
    return f"Nie można połączyć się z Neo4j: {exc}"


@app.get("/")
async def people_page(
    request: Request,
    edit: str | None = None,
    error: str | None = None,
):
    people = []
    selected_person = None
    error_message = None

    if error == "neo4j":
        error_message = "Operacja nie powiodła się, bo Neo4j nie odpowiedział poprawnie."

    try:
        driver = neo4j_connection.get_driver()
        if neo4j_connection.startup_error:
            await driver.verify_connectivity()
            neo4j_connection.startup_error = None

        await ensure_constraints(driver)
        people = await list_people(driver)
        selected_person = await get_person(driver, edit) if edit else None
    except (Neo4jError, ServiceUnavailable, RuntimeError) as exc:
        error_message = neo4j_error_message(exc)

    return templates.TemplateResponse(
        request=request,
        name="people.html",
        context={
            "people": people,
            "selected_person": selected_person,
            "is_edit_mode": selected_person is not None,
            "error_message": error_message,
        },
    )


@app.post("/people/create")
async def create_person_action(
    name: str = Form(...),
    email: str = Form(""),
    note: str = Form(""),
):
    try:
        driver = neo4j_connection.get_driver()
        await create_person(
            driver=driver,
            name=name.strip(),
            email=email.strip(),
            note=note.strip(),
        )
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/people/update")
async def update_person_action(
    person_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(""),
    note: str = Form(""),
):
    try:
        driver = neo4j_connection.get_driver()
        await update_person(
            driver=driver,
            person_id=person_id,
            name=name.strip(),
            email=email.strip(),
            note=note.strip(),
        )
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/people/delete")
async def delete_person_action(person_id: str = Form(...)):
    try:
        driver = neo4j_connection.get_driver()
        await delete_person(driver, person_id)
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.get("/health")
async def health():
    try:
        driver = neo4j_connection.get_driver()
        await driver.verify_connectivity()
    except (Neo4jError, ServiceUnavailable, RuntimeError) as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "detail": neo4j_error_message(exc)},
        )
    return {"status": "ok"}
