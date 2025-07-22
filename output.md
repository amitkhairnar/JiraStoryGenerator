
# Admin - Create New User Page with Backend Integration

**Story Points:** 8

---

## User Story
As an Administrator, I want to create a new user account via a dedicated page so that I can efficiently onboard new members to the platform.

## Acceptance Criteria
- Given I am an authenticated Administrator, when I navigate to the user management section, then I should see an option to 'Create New User'.
- Given I am on the 'Create New User' page, the form must contain input fields for First Name, Last Name, and Email Address, using 'Starlight' design system components.
- Given I have filled out the form with valid data, when I click the 'Create' button, then a POST request is sent to a new FastAPI endpoint (`/api/v1/users`).
- Given the user is created successfully in the PostgreSQL database via SQLAlchemy, then I should be redirected to the user list and see a success confirmation message.
- Given I attempt to create a user with an email that already exists, then the API should return an error and a user-friendly message should be displayed on the form.
- Given I submit the form with invalid or missing data (e.g., empty email), then inline validation errors should be displayed next to the respective fields.
- All user-facing text on the page (labels, buttons, messages) must be internationalized (i18n-ready).
- Unit tests for the new frontend components and the backend endpoint must achieve at least 80% code coverage.
