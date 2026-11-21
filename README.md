# Smart Service Desk Management System

Name: <YOUR NAME>

Participant ID: <YOUR ID>

## Problem Statement
Employees need a simple, reliable way to create IT support requests and preserve their status. The application provides a menu-based Python CLI for creating, viewing, searching, resolving, and tracking requests.

## Objective
This project demonstrates Python OOP, custom exceptions, JSON persistence, SOLID, Domain-Driven Design, role-based authentication, automated testing, Git, and GitHub workflows.

## Implemented Features
- Authenticated login with `ADMIN` and `EMPLOYEE` roles
- Create unique service requests
- Automatically use `OPEN` status
- View all requests
- Search by Request ID
- Resolve only as an administrator
- Prevent resolving the same request twice
- View only the logged-in employee's previous requests
- Persist requests in `data/requests.json`
- Store user passwords as salted PBKDF2-SHA256 hashes

## Technology Stack
- Python 3
- Standard-library `unittest`
- JSON file storage
- Git and GitHub

## Architecture

### Domain
`ServiceRequest` owns request data and behavior. `resolve()` changes `OPEN` to `RESOLVED`; JSON is not used here.

### Application
`RequestService` implements create, view, search, resolve, and personal-history use cases. It depends on `AbstractRepository`, not a concrete JSON class.

### Infrastructure
`FileRepository` implements JSON loading, saving, missing-file handling, empty-file handling, and corrupted-file reporting.

### Presentation
`AuthenticationService` verifies credentials. `MainApplication` inherits `RequestService` and handles login and CLI input/output.

## Folder Structure

```text
smart-service-desk/
├── application/
│   ├── __init__.py
│   └── request_service.py
├── data/
│   ├── requests.json
│   └── users.json
├── domain/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── repository.py
│   └── service_request.py
├── infrastructure/
│   ├── __init__.py
│   └── file_repository.py
├── presentation/
│   ├── __init__.py
│   ├── auth.py
│   └── main_app.py
├── tests/
│   ├── __init__.py
│   ├── test_file_repository.py
│   ├── test_request_service.py
│   └── test_service_request.py
├── .gitignore
├── main.py
└── README.md
```

## Concepts Used

| Concept | Where it is used |
|---|---|
| OOP | `ServiceRequest` uses private attributes, properties, a constructor, serialization methods, and `resolve()` domain behavior. |
| Exception handling | Custom exceptions such as `DuplicateRequestError`, `RequestNotFoundError`, `InvalidPriorityError`, and `AuthorizationError` provide controlled CLI errors. |
| File handling | `FileRepository` reads and writes `data/requests.json` and handles missing, empty, BOM-prefixed, and corrupted JSON safely. |
| SOLID | SRP separates domain, application, infrastructure, and presentation jobs; DIP makes `RequestService` depend on `AbstractRepository` rather than JSON implementation. |
| DDD | Domain rules live in `ServiceRequest`, use cases in `RequestService`, JSON storage in infrastructure, and input/output in presentation. |
| Git | Development is maintained on `development`, meaningful commits record each layer, and tested work is merged into `main`. |

## Authentication
Demo accounts:

| Username | Password | Role |
|---|---|---|
| `admin` | `Admin@123` | ADMIN |
| `employee` | `Employee@123` | EMPLOYEE |

These are deliberately non-personal demonstration credentials. Passwords are never stored in plaintext.

## Installation
Python 3 is required. No third-party package is required.

```powershell
cd into the project folder
python main.py
```

## Automated Tests

```powershell
python -m unittest discover -s tests -v
```

Tests use temporary directories; they do not damage real project request data.

## Sample CLI Flow

```text
SMART SERVICE DESK LOGIN
Username: employee
Password: ********
Login successful.

1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit
6. View My Previous Requests

Enter Request ID: SR101
Enter Employee Name: Rahul
Enter Issue: Laptop is not starting
Enter Priority: HIGH
Service Request created successfully.
SR101 | Rahul | Laptop is not starting | HIGH | OPEN
```

## Persistence and Errors
`data/requests.json` is loaded at repository use time and written after creation or resolution. Missing and empty files are treated as empty repositories. Corrupted JSON produces `RepositoryError`. Custom exceptions provide clear duplicate, missing, priority, authentication, authorization, and resolved-state messages.

## Git Branch and Merge Strategy
Development work was done on the `development` branch in several meaningful commits covering project structure, domain logic, JSON repository, application services, authentication, CLI integration, tests, and documentation. A Pull Request from `development` to `main` was raised on GitHub and merged; the final code is on `main`. The complete branch and commit history can be shown with:

```powershell
git log --oneline --graph --all
```

## GitHub Pull Request
1. Push `development` to GitHub.
2. Open a Pull Request from `development` into `main`.
3. Review the changes and merge the Pull Request.
4. Pull main locally and verify:

```powershell
git checkout main
git pull origin main
git log --oneline --graph --all
git branch -a
git status
```

## Git Commit Example History
The repository should contain separate meaningful commits for structure, domain logic, repository storage, application use cases, authentication/CLI, tests, and documentation.

## Limitations
This is an educational CLI application with local JSON storage. It is not intended for concurrent users or production database workloads.

## Submission Evidence to Capture
- Login as employee and perform all assigned demonstration steps
- Employee attempt to resolve must show authorization error
- Login as admin and resolve request
- Resolve the request again to show the already-resolved message
- Restart and search to prove `RESOLVED` persisted
- `git log --oneline --graph --all`
- `git branch -a`
- `git status`
- GitHub Pull Request and merge confirmation

## Extra Features (beyond the assignment)

1. Login with `ADMIN` and `EMPLOYEE` roles.
2. Only an admin can resolve a request.
3. Passwords are stored as salted PBKDF2-SHA256 hashes in `data/users.json`.
4. An abstract repository class (`AbstractRepository`) is implemented by the JSON `FileRepository` class.
5. `MainApplication` inherits `RequestService`.
6. Menu option 6, `View My Previous Requests`, shows only the logged-in user's requests using the `created_by` field.
7. Automated unit tests are provided in `tests/`.
8. Missing, empty, and corrupted JSON files are handled safely.

### Default Login Accounts

| Username | Password | Role |
|---|---|---|
| `admin` | `Admin@123` | ADMIN |
| `employee` | `Employee@123` | EMPLOYEE |
