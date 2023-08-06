""" Action Queue Process Controller Definition """

from rowantree.contracts import ActionQueue

from .abstract_controller import AbstractController


class ActionQueueProcessController(AbstractController):
    """
    Action Queue Process Controller
    Processes the requested action queue.

    Methods
    -------
    execute(self, action_queue: ActionQueue) -> None
        Execute the controller.
    """

    def execute(self, request: ActionQueue) -> None:
        """
        Processes the requested action queue.

        Parameters
        ----------
        request: ActionQueue
            The process action queue.
        """

        self.dao.process_action_queue(action_queue=request)
