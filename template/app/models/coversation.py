from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
import uuid


class Conversation(Model):
    __keyspace__ = "ufo"

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.Text(required=True)
    agent_id = columns.Text()
    messages = columns.List(columns.Text)
    created_at = columns.DateTime()
