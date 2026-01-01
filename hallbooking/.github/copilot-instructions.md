<!-- Repository-specific instructions for AI coding assistants. Keep this concise (20-50 lines).
     This file guides Copilot/GitHub AI to be immediately productive in this Django project. -->

# Hall Booking System — Copilot Instructions

- Project root: repository contains a Django project in `hallbooking/` and an app `bookings/`.
- Purpose: Manage bookings for 4 college halls using Django (backend), SQLite (DB), and HTML/CSS/JS (frontend).

## Big picture
- `hallbooking/settings.py` configures the project (SQLite DB, static files at `static/`).
- `bookings/models.py` defines two key models: `Hall` and `Booking`. Booking validation lives in `Booking.clean()` and `save()`.
- `bookings/views.py` contains the primary HTTP endpoints (index, hall_detail, book_hall, my_bookings, cancel_booking, booking_confirmation, check_availability).
- Templates live in `templates/` and `bookings/templates/bookings/` (use `base.html` for shared layout).
- Static assets are under `static/css/style.css` and `static/js/main.js`.

## When making changes
- Preserve model validation in `Booking.clean()` — it enforces date, capacity, and time-conflict rules.
- Update forms and templates together when adding/removing model fields. Templates rely on specific variable names: e.g., `hall`, `bookings`, `booking`.
- Use Django `messages` for user-visible feedback; templates expect `messages` to be present.
- AJAX availability endpoint: `GET /api/check-availability/?hall_id=<id>&date=<YYYY-MM-DD>` returns JSON `{available: true|false}`. Keep response format unchanged if modifying frontend.

## Developer workflows (how to run & test)
- Install deps: `pip install -r requirements.txt`.
- Migrate DB: `python manage.py migrate`.
- Create superuser: `python manage.py createsuperuser`.
- Initialize sample halls: `python init_db.py` (creates 4 halls used by UI).
- Run server: `python manage.py runserver`.
- Run tests: `python manage.py test` (small model tests are present in `bookings/tests.py`).

## Conventions & patterns
- Templates: use `base.html` (located in `templates/`) as the base. App templates are in `bookings/templates/bookings/`.
- Forms are plain HTML POST forms (no Django forms used). Server-side validation is authoritative.
- Client-side validation and AJAX are in `static/js/main.js`; keep the `checkAvailability` and availability DOM IDs (`availabilityCheck`, `availabilityText`) stable.
- CSS variables are defined at top of `static/css/style.css`; change theme colors there.

## Integration points & external dependencies
- No external services configured by default. Email backend is console by default (see `.env.example` and `settings.py` comments). If adding email, update `settings.py` accordingly.
- Database is SQLite at `db.sqlite3` by default.

## Safe edits and testing checklist for PRs
- If models change, add migrations (`makemigrations`) and include them in PR.
- Run `python manage.py migrate` and `python manage.py test` locally.
- Verify templates render: homepage `/`, hall detail page `/hall/<id>/`, and booking flow end-to-end.
- Verify admin behavior: `python manage.py createsuperuser`, then `/admin/` to approve bookings.
- Keep `DEBUG=True` only for development; remember to document changes to `settings.py` when preparing production deploy.

## Files to inspect first when troubleshooting
- `bookings/models.py` — validation and unique constraints
- `bookings/views.py` — booking flow and availability endpoint
- `templates/base.html` — shared layout and messages
- `static/js/main.js` — client-side behavior for forms and availability
- `init_db.py` — sample data used in demos/tests

## Example quick tasks (how-to snippets)
- Add a model field: update `bookings/models.py` → `python manage.py makemigrations` → `python manage.py migrate` → update templates that reference the model.
- Change availability response to include existing bookings: modify `bookings/views.check_availability` and keep frontend JSON parsing intact.

If anything in these instructions is unclear or you want the file tailored (shorter/longer or stricter rules), tell me what to change.