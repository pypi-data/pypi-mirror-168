from aries_cloudagent.messaging.agent_message import AgentMessage, AgentMessageSchema
from marshmallow import EXCLUDE, fields
from peopledata_did.v1_0.message_types import PROTOCOL_PACKAGE, READ_DID_RESPONSE
from peopledata_did.v1_0.models.diddoc_model import (
    peopledataDIDResponseBody,
    peopledataDIDResponseBodySchema,
)
from peopledata_did.v1_0.utils.regex import peopledata_DID

# Handler class for /peopledata/v1.0/read-did-response
HANDLER_CLASS = (
    f"{PROTOCOL_PACKAGE}.handlers" ".read_did_response_handler.ReadDIDResponseHandler"
)


class ReadDIDResponseMessage(AgentMessage):
    """
    Message class for response to reading a DID.
    """

    class Meta:

        # Handler class that can handle this message
        handler_class = HANDLER_CLASS

        # Message type
        message_type = READ_DID_RESPONSE

        # Message schema class
        schema_class = "ReadDIDResponseMessageSchema"

    def __init__(
        self, *, from_did, to_did, created_time, body: peopledataDIDResponseBody, **kwargs
    ):
        """
        Initialize a ReadDIDResponseMessage message instance.
        """
        super().__init__(**kwargs)

        # Set attributes
        self.from_did = from_did
        self.to_did = to_did
        self.created_time = created_time
        self.body = body


class ReadDIDResponseMessageSchema(AgentMessageSchema):
    """
    Schema class for response to reading a DID.
    """

    class Meta:
        # Model class
        model_class = ReadDIDResponseMessage

        # Unknown fields to exclude from the schema (handled by marshmallow)
        unknown = EXCLUDE

    # From DID
    from_did = fields.Str(data_key="from", **peopledata_DID)

    # To DID
    to_did = fields.Str(data_key="to", **peopledata_DID)

    # Created Time
    created_time = fields.Str(data_key="created_time")

    # Message body
    body = fields.Nested(peopledataDIDResponseBodySchema, required=True)
