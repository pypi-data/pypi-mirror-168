""" User Delete Controller Definition """

from .abstract_controller import AbstractController


class UserDeleteController(AbstractController):
    """
    User Delete Controller
    Deletes a user.

    Methods
    -------
    execute(self, user_guid: str) -> None
        Executes the command.
    """

    def execute(self, user_guid: str) -> None:
        """
        Deletes a user.
        TODO: the underlying calls need to provide more context on status of this call.

        Parameters
        ----------
        user_guid: str
            The target user guid.
        """

        self.dao.user_delete(user_guid=user_guid)
