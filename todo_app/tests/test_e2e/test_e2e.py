from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta


class TodoAppE2ETest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
        cls.driver.implicitly_wait(10)  # Implicit wait for all elements
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def authenticate(self):
        """Perform authentication using HTTP Basic Auth."""
        auth_url = f'{self.live_server_url}/api/todos/'.replace('://', f'://{self.username}:{self.password}@')
        self.driver.get(auth_url)

    def wait_for_element(self, by, identifier, timeout=10):
        """Wait for an element to be visible."""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, identifier)))

    def create_todo_item(self):
        """Step 1: Create a Todo item."""
        self.authenticate()

        # Switch to the "Raw data" tab
        raw_tab = self.wait_for_element(By.LINK_TEXT, "Raw data")
        raw_tab.click()

        # Fill the "Raw data" form with JSON content
        create_data = {
            "title": "E2E Test Todo",
            "description": "Todo created via E2E test.",
            "due_date": "2024-12-06T00:00:00+05:30",
            "tags": [{"name": "E2E"}, {"name": "Test"}],
            "status": "OPEN"
        }
        raw_content = self.wait_for_element(By.ID, "id__content")
        raw_content.clear()
        raw_content.send_keys(json.dumps(create_data))

        # Click the "POST" button
        post_button = self.driver.find_element(By.XPATH, "//button[text()='POST']")
        post_button.click()

        # Verify the Todo item was created
        response_pre = self.wait_for_element(By.TAG_NAME, "pre")
        response_data = json.loads(response_pre.text)
        self.assertIn("E2E Test Todo", response_pre.text)
        todo_id = response_data["id"]
        print(f"Todo Item Created with ID: {todo_id}")
        return todo_id

    def view_todo_items(self):
        """Step 2: View all Todo items."""
        self.authenticate()

        # Locate and click the GET button to view all Todos
        get_button = self.wait_for_element(By.XPATH, "//button[text()='GET']")
        get_button.click()

        # Wait for the response to load and capture the displayed list
        response_pre = self.wait_for_element(By.TAG_NAME, "pre")

        # Assert that the created Todo item appears in the list
        self.assertIn("E2E Test Todo", response_pre.text)
        print("Verified the Todo item appears in the list view.")

    def update_todo_item(self, todo_id):
        """Step 3: Update a Todo item."""
        update_url = f"{self.live_server_url}/api/todos/{todo_id}/".replace(
            "://", f"://{self.username}:{self.password}@"
        )
        self.driver.get(update_url)

        # Switch to the "Raw data" tab for update
        raw_tab = self.wait_for_element(By.LINK_TEXT, "Raw data")
        raw_tab.click()

        # Update the "Raw data" form with JSON content
        update_data = {
            "id": todo_id,
            "title": "Updated E2E Test Todo",
            "description": "Todo updated via E2E test.",
            "due_date": "2024-12-06T00:00:00+05:30",
            "tags": [{"name": "Updated"}, {"name": "E2E"}],
            "status": "WORKING",
        }
        raw_content = self.wait_for_element(By.ID, "id__content")
        raw_content.clear()
        raw_content.send_keys(json.dumps(update_data))

        # Click the "PUT" button
        put_button = self.driver.find_element(By.XPATH, "//button[text()='PUT']")
        put_button.click()

        # Verify the Todo item was updated
        response_pre = self.wait_for_element(By.TAG_NAME, "pre")
        self.assertIn("Updated E2E Test Todo", response_pre.text)
        print("Verified Todo item was updated.")

    def delete_todo_item(self, todo_id):
        """Step 4: Delete a Todo item."""
        delete_url = f"{self.live_server_url}/api/todos/{todo_id}/".replace(
            "://", f"://{self.username}:{self.password}@"
        )
        self.driver.get(delete_url)

        # Locate and click the DELETE button
        delete_button = self.driver.find_element(By.XPATH, "//button[text()='DELETE']")
        delete_button.click()

        # Confirm the deletion in the modal
        confirm_delete_button = self.wait_for_element(By.CSS_SELECTOR, ".modal-content .btn-danger")
        confirm_delete_button.click()

        # Verify the Todo item was deleted
        self.authenticate()
        response_pre = self.wait_for_element(By.TAG_NAME, "pre")
        self.assertNotIn("Updated E2E Test Todo", response_pre.text)
        print("Verified Todo item was deleted successfully.")

    def test_full_todo_workflow(self):
        """Perform the full E2E workflow."""
        todo_id = self.create_todo_item()
        self.view_todo_items()
        self.update_todo_item(todo_id)
        self.delete_todo_item(todo_id)
