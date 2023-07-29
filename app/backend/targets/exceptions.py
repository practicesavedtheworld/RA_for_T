from app.backend.exceptions.target_exceptions import BaseTargetException


class NoTargetFound(BaseTargetException):
    detail = "Targets not found or it has been deleted"


class TaskAlreadyRemoved(BaseTargetException):
    detail = "There is no task found or it has been removed"
