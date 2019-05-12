from qozyd.context import ContextExecutable
from qozyd.utils.events import new_thing_found
from qozyd.models import Qozy
from qozyd.models.notifications import Notification
import transaction


class NotificationManager(ContextExecutable):
    def __init__(self, db):
        self.db = db
    
    def start(self):
        self.zeo_connection = self.db.open()
        self.zeo_connection.sync()

        self.root = self.zeo_connection.root()["app_root"]

        new_thing_found.append(self.new_thing_found)

    def stop(self):
        new_thing_found.remove(self.new_thing_found)
        self.zeo_connection.close()

    def new_thing_found(self, thing):
        notification = Notification("qozy.thing", "New thing", "New thing found, configure now")
        
        self.root.add_notification(notification)
        transaction.commit()
