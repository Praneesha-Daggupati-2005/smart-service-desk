from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestError,
    RequestNotFoundError,
    InvalidPriorityError,
    InvalidCredentialsError,
    AuthorizationError,
    AlreadyResolvedError, #df
    InvalidMenuChoiceError,
    RepositoryError,
)


class MainApplication(RequestService):
    """Thin presentation class that inherits the application use cases."""

    def __init__(self, repository, auth_service):
        super().__init__(repository)
        self.auth_service = auth_service
        self.current_user = None

    def login(self):
        print("SMART SERVICE DESK LOGIN")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        self.current_user = self.auth_service.authenticate(username, password)

    def _print_request(self, request):
        print(
            f"{request.request_id} | {request.employee_name} | "
            f"{request.issue} | {request.priority} | {request.status}"
        )

    def run(self):
        while True:
            try:
                self.login()
                print("Login successful.")
                break
            except InvalidCredentialsError:
                print("Invalid username or password. Please try again.")
            except RepositoryError as exc:
                print(str(exc))

        while True:
            print("\nSMART SERVICE DESK SYSTEM")
            print("1. Create Service Request")
            print("2. View All Requests")
            print("3. Search Request")
            print("4. Resolve Request")
            print("5. Exit")
            print("6. View My Previous Requests")

            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    request_id = input("Enter Request ID: ").strip()
                    employee_name = input("Enter Employee Name: ").strip()
                    issue = input("Enter Issue: ").strip()
                    priority = input("Enter Priority: ").strip()
                    request = self.create_request(
                        request_id,
                        employee_name,
                        issue,
                        priority,
                        self.current_user["username"],
                    )
                    print("Service Request created successfully.")
                    self._print_request(request)

                elif choice == "2":
                    requests = self.view_requests()
                    if not requests:
                        print("No service requests found.")
                    else:
                        for request in requests:
                            self._print_request(request)

                elif choice == "3":
                    request_id = input("Enter Request ID: ").strip()
                    request = self.search_request(request_id)
                    self._print_request(request)

                elif choice == "4":
                    request_id = input("Enter Request ID: ").strip()
                    request = self.resolve_request(
                        request_id,
                        self.current_user["username"],
                        self.current_user["role"],
                    )
                    print("Request resolved successfully.")
                    self._print_request(request)

                elif choice == "5":
                    print("Goodbye!")
                    break

                elif choice == "6":
                    requests = self.view_my_requests(self.current_user["username"])
                    if not requests:
                        print("You have not created any previous requests.")
                    else:
                        for request in requests:
                            self._print_request(request)

                else:
                    print("Invalid menu choice.")

            except InvalidMenuChoiceError:
                print("Invalid menu choice. Please select a valid option.")
            except DuplicateRequestError as exc:
                print(str(exc))
            except RequestNotFoundError as exc:
                print(str(exc))
            except InvalidPriorityError as exc:
                print(str(exc))
            except AuthorizationError as exc:
                print(str(exc))
            except AlreadyResolvedError as exc:
                print(str(exc))
            except RepositoryError as exc:
                print(str(exc))
            except ValueError as exc:
                print(str(exc))
