from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from neo4j.exceptions import Neo4jError, ServiceUnavailable

from app.cities_service import (
    create_city,
    delete_city,
    get_city,
    list_cities,
    update_city,
)
from app.db import neo4j_connection, neo4j_lifespan
from app.people_service import (
    create_person,
    delete_person,
    ensure_constraints,
    get_person,
    list_people,
    update_person,
)
from app.relationships_service import (
    assign_person_to_city,
    list_lives_in_relationships,
    remove_lives_in_relationship,
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
    edit_city: str | None = None,
    error: str | None = None,
):
    people = []
    cities = []
    relationships = []
    selected_person = None
    selected_city = None
    error_message = None

    if error == "neo4j":
        error_message = "Operacja nie powiodła się, bo Neo4j nie odpowiedział poprawnie."
    elif error == "validation":
        error_message = "Uzupełnij wymagane pola formularza."
    elif error == "not_found":
        error_message = "Nie znaleziono wybranej osoby albo miasta."

    try:
        driver = neo4j_connection.get_driver()
        if neo4j_connection.startup_error:
            await driver.verify_connectivity()
            neo4j_connection.startup_error = None

        await ensure_constraints(driver)
        people = await list_people(driver)
        cities = await list_cities(driver)
        relationships = await list_lives_in_relationships(driver)
        selected_person = await get_person(driver, edit) if edit else None
        selected_city = await get_city(driver, edit_city) if edit_city else None
    except (Neo4jError, ServiceUnavailable, RuntimeError) as exc:
        error_message = neo4j_error_message(exc)

    return templates.TemplateResponse(
        request=request,
        name="people.html",
        context={
            "people": people,
            "cities": cities,
            "relationships": relationships,
            "selected_person": selected_person,
            "selected_city": selected_city,
            "is_person_edit_mode": selected_person is not None,
            "is_city_edit_mode": selected_city is not None,
            "error_message": error_message,
        },
    )


@app.post("/people/create")
async def create_person_action(
    name: str = Form(...),
    email: str = Form(""),
    note: str = Form(""),
):
    name_value = name.strip()
    if not name_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        await create_person(
            driver=driver,
            name=name_value,
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
    name_value = name.strip()
    person_id_value = person_id.strip()
    if not person_id_value or not name_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        await update_person(
            driver=driver,
            person_id=person_id_value,
            name=name_value,
            email=email.strip(),
            note=note.strip(),
        )
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/people/delete")
async def delete_person_action(person_id: str = Form(...)):
    person_id_value = person_id.strip()
    if not person_id_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        await delete_person(driver, person_id_value)
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/cities/create")
async def create_city_action(
    name: str = Form(...),
    country: str = Form(""),
    note: str = Form(""),
):
    name_value = name.strip()
    if not name_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        await create_city(
            driver=driver,
            name=name_value,
            country=country.strip(),
            note=note.strip(),
        )
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/cities/update")
async def update_city_action(
    city_id: str = Form(...),
    name: str = Form(...),
    country: str = Form(""),
    note: str = Form(""),
):
    city_id_value = city_id.strip()
    name_value = name.strip()
    if not city_id_value or not name_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        await update_city(
            driver=driver,
            city_id=city_id_value,
            name=name_value,
            country=country.strip(),
            note=note.strip(),
        )
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/cities/delete")
async def delete_city_action(city_id: str = Form(...)):
    city_id_value = city_id.strip()
    if not city_id_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        await delete_city(driver, city_id_value)
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/relationships/lives-in/create")
async def create_lives_in_relationship_action(
    person_id: str = Form(...),
    city_id: str = Form(...),
):
    person_id_value = person_id.strip()
    city_id_value = city_id.strip()
    if not person_id_value or not city_id_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        created = await assign_person_to_city(
            driver=driver,
            person_id=person_id_value,
            city_id=city_id_value,
        )
    except (Neo4jError, ServiceUnavailable, RuntimeError):
        return RedirectResponse("/?error=neo4j", status_code=303)

    if not created:
        return RedirectResponse("/?error=not_found", status_code=303)

    return RedirectResponse("/", status_code=303)


@app.post("/relationships/lives-in/delete")
async def delete_lives_in_relationship_action(
    person_id: str = Form(...),
    city_id: str = Form(...),
):
    person_id_value = person_id.strip()
    city_id_value = city_id.strip()
    if not person_id_value or not city_id_value:
        return RedirectResponse("/?error=validation", status_code=303)

    try:
        driver = neo4j_connection.get_driver()
        await remove_lives_in_relationship(
            driver=driver,
            person_id=person_id_value,
            city_id=city_id_value,
        )
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
