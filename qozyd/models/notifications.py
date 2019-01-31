from persistent import Persistent
from datetime import datetime


class Notification(Persistent):
    def __init__(self, context_id, title, summary):
        self.context_id = context_id
        self.title = title
        self.summary = summary
        self.created = datetime.now()

    @property
    def dismissable(self):
        return True

    def __json__(self):
        return {
            "contextId": self.context_id,
            "type": self.__class__.__name__,
            "dismissable": self.dismissable,
            "created": self.created,
            "title": self.title,
            "summary": self.summary,
        }


class ExecutionStateNotification(Notification):
    STATE_PENDING = "PENDING"
    STATE_RUNNING = "RUNNING"
    STATE_SUCCESS = "SUCCESS"
    STATE_FAILURE = "FAILURE"

    FINISH_STATES = (STATE_SUCCESS, STATE_FAILURE)

    def __init__(self, context_id, title, summary):
        super().__init__(context_id, title, summary)

        self.state = self.STATE_PENDING
        self.percentage_finished = None

    @property
    def dismissable(self):
        return self.state in self.FINISH_STATES
    
    def __json__(self):
        return {
            **super().__json__(),
            **{
                "state": self.state,
                "percentageFinished": self.percentage_finished,
            }
        }
