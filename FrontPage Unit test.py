def test_welcome_window_initialization(self):
    # Verifies that the WelcomeWindow loads correctly
    # with the required title, welcome message, and navigation buttons

    # Check window properties
    self.assertEqual(
        self.window.windowTitle(),
        "Study Smart"
    )

    self.assertEqual(self.window.width(), 1200)
    self.assertEqual(self.window.height(), 800)

    # Check welcome message
    labels = self.window.findChildren(QLabel)

    found = False
    for label in labels:
        if label.text() == "Welcome to Study Smart":
            found = True

    self.assertTrue(found)

    # Check buttons exist with correct text
    self.assertEqual(
        self.window.signup_button.text(),
        "Sign Up"
    )

    self.assertEqual(
        self.window.login_button.text(),
        "Log In"
    )

    # Check that navigation buttons are displayed on screen 
    self.assertTrue(
        self.window.signup_button.isVisible()
    )

    self.assertTrue(
        self.window.login_button.isVisible()
    )
