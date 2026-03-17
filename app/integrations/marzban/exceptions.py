class MarzbanError(Exception):
    """Base Marzban integration error."""


class MarzbanAuthenticationError(MarzbanError):
    """Raised when Marzban authentication fails."""


class MarzbanUnavailableError(MarzbanError):
    """Raised when Marzban cannot be reached."""
