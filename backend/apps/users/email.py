from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = "users/email/activation.html"


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "users/email/confirmation.html"


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "users/email/password_reset.html"


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "users/email/password_changed_confirmation.html"


class UsernameChangedConfirmationEmail(email.UsernameChangedConfirmationEmail):
    template_name = "users/email/username_changed_confirmation.html"


class UsernameResetEmail(email.UsernameResetEmail):
    template_name = "users/email/username_reset.html"
