from pathlib import Path
import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class SppuPortalService:
    """
    Handles the authenticated SPPU College portal using Playwright.

    Login is intentionally manual:
    - The application opens the SPPU login page.
    - User enters username, password and CAPTCHA.
    - Once login succeeds, the service navigates to College Ledger.
    """

    LOGIN_URL = (
        "https://hallticketnew.unipune.ac.in/"
        "College/College/CollegeLogin"
    )

    LEDGER_URL = (
        "https://hallticketnew.unipune.ac.in/"
        "College/CollegeLed/CollegeLedger"
    )

    LOGIN_PATH = "/College/College/CollegeLogin"

    EXAM_PERIOD_SELECTOR = "#ExamPeriodText"
    COURSE_SELECTOR = "#Course"
    BRANCH_SELECTOR = "#Branchcode"
    DOWNLOAD_SELECTOR = "#btn"

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    # ---------------------------------------------------------
    # Connection / Login
    # ---------------------------------------------------------

    def connect(self, status_callback=None):
        """
        Opens the SPPU login page and waits for the user
        to complete the normal login process.
        """

        self._status(
            status_callback,
            "Opening SPPU College Login..."
        )

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.context = self.browser.new_context(
            accept_downloads=True
        )

        self.page = self.context.new_page()

        self.page.goto(
            self.LOGIN_URL,
            wait_until="domcontentloaded"
        )

        self._status(
            status_callback,
            "Please log in to SPPU in the browser window..."
        )

        self._wait_for_login(status_callback)

        self._status(
            status_callback,
            "Login detected. Opening College Ledger..."
        )

        self.page.goto(
            self.LEDGER_URL,
            wait_until="domcontentloaded"
        )

        self._wait_for_ledger_page()

        self._status(
            status_callback,
            "SPPU Ledger page loaded."
        )

        periods = self.get_exam_periods()

        courses = self.get_courses()

        self._status(
            status_callback,
            "Exam periods and course levels loaded."
        )

        return periods, courses

    def _wait_for_login(self, status_callback=None):
        """
        Wait until the login URL is left.

        The user completes the CAPTCHA manually.
        """

        timeout_seconds = 300
        start = time.monotonic()

        while True:

            if self.page.is_closed():
                raise RuntimeError(
                    "The SPPU browser window was closed."
                )

            current_url = self.page.url

            if self.LOGIN_PATH not in current_url:
                return

            elapsed = time.monotonic() - start

            if elapsed >= timeout_seconds:
                raise TimeoutError(
                    "SPPU login timed out after 5 minutes."
                )

            self._status(
                status_callback,
                "Waiting for SPPU login..."
            )

            time.sleep(1)

    def _wait_for_ledger_page(self):
        """
        Navigate/verify that the authenticated ledger page
        is available.
        """

        try:
            self.page.wait_for_selector(
                self.EXAM_PERIOD_SELECTOR,
                timeout=30000
            )

        except PlaywrightTimeoutError as exc:
            if self.LOGIN_PATH in self.page.url:
                raise RuntimeError(
                    "SPPU login was not completed."
                ) from exc

            raise RuntimeError(
                "SPPU Ledger page did not load correctly."
            ) from exc

    # ---------------------------------------------------------
    # Dropdown data
    # ---------------------------------------------------------

    def get_exam_periods(self):
        """
        Reads Exam Period directly from the SPPU page.

        SPPU source:
            #ExamPeriodText

        Values come from:
            ../CollegeLed/ExamPeriod
        """

        self._wait_for_options(
            self.EXAM_PERIOD_SELECTOR
        )

        return self._get_options(
            self.EXAM_PERIOD_SELECTOR
        )

    def get_courses(self):
        """
        Reads Course / Level directly from SPPU.

        Current SPPU values include:
            FE
            SE
            TE
            BE

        The actual values are obtained dynamically.
        """

        self._wait_for_options(
            self.COURSE_SELECTOR
        )

        return self._get_options(
            self.COURSE_SELECTOR
        )

    def get_branches(self, course_value):
        """
        Selects the Course / Level.

        SPPU then calls Fill_Branch and populates
        #Branchcode.
        """

        if not course_value:
            raise ValueError(
                "A Course / Level must be selected."
            )

        self._status(
            None,
            "Loading branches from SPPU..."
        )

        self.page.select_option(
            self.COURSE_SELECTOR,
            course_value
        )

        self.page.wait_for_function(
            """
            () => {
                const select = document.querySelector(
                    '#Branchcode'
                );

                if (!select) {
                    return false;
                }

                return select.options.length > 1;
            }
            """,
            timeout=30000
        )

        return self._get_options(
            self.BRANCH_SELECTOR
        )

    def _wait_for_options(self, selector):
        """
        Wait until a select contains at least one real
        option in addition to the placeholder.
        """

        self.page.wait_for_function(
            """
            (selector) => {
                const select = document.querySelector(selector);

                if (!select) {
                    return false;
                }

                return select.options.length > 1;
            }
            """,
            selector,
            timeout=30000
        )

    def _get_options(self, selector):
        """
        Returns:
            [
                {
                    "value": "...",
                    "text": "..."
                }
            ]
        """

        return self.page.locator(
            f"{selector} option"
        ).evaluate_all(
            """
            options => options
                .map(option => ({
                    value: option.value,
                    text: option.textContent.trim()
                }))
                .filter(option =>
                    option.value !== "00" &&
                    option.text !== "" &&
                    !option.text.includes("Select")
                )
            """
        )

    # ---------------------------------------------------------
    # Ledger download
    # ---------------------------------------------------------

    def download_ledger(
        self,
        exam_period,
        course_value,
        branch_value,
        status_callback=None,
    ):
        """
        Selects the three SPPU parameters and submits
        the actual CollegeLedger form.
        """

        if not exam_period:
            raise ValueError(
                "Exam Period is required."
            )

        if not course_value:
            raise ValueError(
                "Course / Level is required."
            )

        if not branch_value:
            raise ValueError(
                "Branch is required."
            )

        self._status(
            status_callback,
            "Preparing SPPU Ledger download..."
        )

        # Select Exam Period.
        self.page.select_option(
            self.EXAM_PERIOD_SELECTOR,
            exam_period
        )

        # Select Course / Level.
        self.page.select_option(
            self.COURSE_SELECTOR,
            course_value
        )

        # Give SPPU's JavaScript a moment to refresh
        # the Branch dropdown.
        self.page.wait_for_function(
            """
            () => {
                const select = document.querySelector(
                    '#Branchcode'
                );

                return select &&
                       select.options.length > 1;
            }
            """,
            timeout=30000
        )

        # Select Branch.
        self.page.select_option(
            self.BRANCH_SELECTOR,
            branch_value
        )

        self._status(
            status_callback,
            "Requesting ledger from SPPU..."
        )

        downloads_dir = (
            Path.cwd() / "downloads"
        )

        downloads_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        try:
            with self.page.expect_download(
                timeout=120000
            ) as download_info:

                self.page.locator(
                    self.DOWNLOAD_SELECTOR
                ).click()

            download = download_info.value

            filename = (
                download.suggested_filename
                or "SPPU_Ledger"
            )

            destination = (
                downloads_dir / filename
            )

            download.save_as(
                str(destination)
            )

            self._status(
                status_callback,
                f"Ledger downloaded: {filename}"
            )

            return str(destination)

        except PlaywrightTimeoutError as exc:

            raise RuntimeError(
                "SPPU did not return a downloadable ledger "
                "within 120 seconds."
            ) from exc

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def _status(callback, message):
        if callback is not None:
            callback(message)

    def close(self):
        """
        Safely close browser and Playwright.
        """

        try:
            if self.context is not None:
                self.context.close()
        except Exception:
            pass

        try:
            if self.browser is not None:
                self.browser.close()
        except Exception:
            pass

        try:
            if self.playwright is not None:
                self.playwright.stop()
        except Exception:
            pass

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None