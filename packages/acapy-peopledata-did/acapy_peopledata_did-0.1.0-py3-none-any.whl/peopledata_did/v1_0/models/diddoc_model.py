import typing

from aries_cloudagent.messaging.models.base import BaseModel, BaseModelSchema
from marshmallow import EXCLUDE, fields
from marshmallow.exceptions import ValidationError
from peopledata_did.v1_0.utils.diddoc import DIDDoc
from peopledata_did.v1_0.utils.regex import peopledataDID
from peopledata_did.v1_0.utils.verification_method import PublicKeyType


class DIDDocWrapper(fields.Field):
    """Field that loads and serializes DIDDoc."""

    def _serialize(self, value, attr, obj, **kwargs):
        """
        Serialize the DIDDoc.

        Args:
            value: The value to serialize

        Returns:
            The serialized DIDDoc

        """
        return value.serialize()

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Deserialize a value into a DIDDoc.

        Args:
            value: The value to deserialize

        Returns:
            The deserialized value

        """
        return DIDDoc.deserialize(value)

    def _validate(self, value: DIDDoc):
        if not value.validate():
            raise ValidationError("peopledata DIDDoc is not valid.")


class peopledataDIDBody(BaseModel):
    class Meta:
        schema_class = "peopledataDIDBodySchema"

    def __init__(self, *, did_doc: DIDDoc, **kwargs):
        super().__init__(**kwargs)
        self.did_doc = did_doc


class peopledataDIDBodySchema(BaseModelSchema):
    class Meta:
        model_class = peopledataDIDBody
        unknown = EXCLUDE

    did_doc = DIDDocWrapper(data_key="did", required=False)


class peopledataDIDDocService(BaseModel):
    """
    Service information for a DID Document.
    """

    class Meta:
        # Schema class
        schema_class = "peopledataDIDDocServiceSchema"

    def __init__(
        self,
        *,
        service_id: str = None,
        service_type: str = None,
        service_priority: int = 0,
        recipient_keys: typing.List[str] = None,
        service_endpoint: str = None,
        **kwargs,
    ):
        """
        Initialize a DID Document Service object.

        Args:
            service_id: The service ID
            service_type: The service type
            service_priority: The service priority
            recipient_keys: The recipient keys
            service_endpoint: The service endpoint
        """

        super().__init__(**kwargs)

        # Service ID
        self.service_id = service_id

        # Service type
        self.service_type = service_type

        # Service priority
        self.service_priority = service_priority

        # Recipient keys
        self.recipient_keys = recipient_keys

        # Service endpoint
        self.service_endpoint = service_endpoint


class peopledataDIDDocServiceSchema(BaseModelSchema):
    """
    Schema for DID Document Service.
    """

    class Meta:

        # Model class
        model_class = peopledataDIDDocService

        # Unknown fields are excluded.
        unknown = EXCLUDE

    # Service ID
    service_id = fields.Str(
        data_key="id", required=True, example=f"did:peopledata:{peopledataDID.EXAMPLE};didcomm"
    )

    # Service type
    service_type = fields.Str(data_key="type", required=True, example="DIDComm")

    # Service priority
    service_priority = fields.Int(data_key="priority", required=True, example=1)

    # Recipient keys
    recipient_keys = fields.List(
        fields.Str(required=True, example=peopledataDID.EXAMPLE),
        data_key="recipientKeys",
        required=True,
    )

    # Service endpoint
    service_endpoint = fields.Str(
        data_key="serviceEndpoint", required=True, example="https://didcomm.org"
    )


class peopledataDIDDocAuthentication(BaseModel):
    """
    Authentication information for a DID Document.
    """

    class Meta:
        # Schema class
        schema_class = "peopledataDIDDocAuthenticationSchema"

    def __init__(
        self, *, authentication_type: str = None, public_key: str = None, **kwargs
    ):
        """
        Initialize a DID Document Authentication object.

        Args:
            authentication_type: The authentication type
            public_key: The public key
        """
        super().__init__(**kwargs)

        # Set attributes
        self.authentication_type = authentication_type
        self.public_key = public_key


class peopledataDIDDocAuthenticationSchema(BaseModelSchema):
    """
    Schema for DID Document Authentication.

    """

    class Meta:

        # Model class
        model_class = peopledataDIDDocAuthentication

        # Unknown fields are excluded.
        unknown = EXCLUDE

    # The authentication type
    authentication_type = fields.Str(
        data_key="type",
        required=True,
        example=PublicKeyType.ED25519_SIG_2018.authn_type,
    )

    # The public key
    public_key = fields.Str(
        data_key="publicKey",
        required=True,
        example=f"did:peopledata:f{peopledataDID.EXAMPLE}#1",
    )


class peopledataDIDDocVerificationMethod(BaseModel):
    """
    A DID Document Verification Method.
    """

    class Meta:
        # Schema class
        schema_class = "peopledataDIDDocVerificationMethodSchema"

    def __init__(
        self,
        *,
        verification_method_id: str = None,
        verification_method_type: str = None,
        controller: str = None,
        public_key_base58: str = None,
        **kwargs,
    ):
        """
        Initialize a DID Document Verification Method.

        Args:
            verification_method_id: The verification method id
            verification_method_type: The verification method type
            controller: The controller
            public_key_base58: The public key base58
        """

        # Initialize the super class
        super().__init__(**kwargs)

        # Set attributes
        self.verification_method_id = verification_method_id
        self.verification_method_type = verification_method_type
        self.controller = controller
        self.public_key_base58 = public_key_base58


class peopledataDIDDocVerificationMethodSchema(BaseModelSchema):
    """
    A DID Document Verification Method Schema.
    """

    class Meta:
        # Schema class
        model_class = peopledataDIDDocVerificationMethod

    # Verification method id
    verification_method_id = fields.Str(
        data_key="id", required=True, example=f"did:peopledata:{peopledataDID.EXAMPLE}#1"
    )

    # Verification method type
    verification_method_type = fields.Str(
        data_key="type", required=True, example=PublicKeyType.ED25519_SIG_2018.ver_type
    )

    # Controller
    controller = fields.Str(
        data_key="controller", required=True, example=f"did:peopledata:{peopledataDID.EXAMPLE}"
    )

    # Public key base58
    public_key_base58 = fields.Str(
        data_key="publicKeyBase58", required=True, example=f"{peopledataDID.EXAMPLE}"
    )


class peopledataDIDDoc(BaseModel):
    """
    peopledata DIDDoc model
    """

    class Meta:
        # Schema class
        schema_class = "peopledataDIDDocSchema"

    def __init__(
        self,
        *,
        context: str = None,
        diddoc_id: str = None,
        verification_method: typing.List[peopledataDIDDocVerificationMethod] = None,
        authentication: typing.List[peopledataDIDDocAuthentication] = None,
        service: typing.List[peopledataDIDDocService] = None,
        **kwargs,
    ):
        """
        Initialize a peopledata DIDDoc model.

        Args:
            context: The DIDDoc context
            diddoc_id: The DIDDoc id
            verification_method: The verification method
            authentication: The authentication method
            service: The service
            kwargs: The extra arguments

        """

        # Call parent constructor
        super().__init__(**kwargs)

        # Set attributes
        self.context = context
        self.diddoc_id = diddoc_id
        self.verification_method = verification_method
        self.authentication = authentication
        self.service = service


class peopledataDIDDocSchema(BaseModelSchema):
    """
    peopledata DIDDoc schema
    """

    class Meta:
        # Model class
        model_class = peopledataDIDDoc

        # Unknown fields are excluded
        unknown = EXCLUDE

    # The DIDDoc context
    context = fields.Str(
        required=True,
        data_key="@context",
        example=DIDDoc.CONTEXT,
        description="The DIDDoc context",
    )

    # The DIDDoc id
    diddoc_id = fields.Str(
        required=True,
        data_key="id",
        example=f"did:peopledata:{peopledataDID.EXAMPLE}",
    )

    # The verification method
    verification_method = fields.List(
        fields.Nested(peopledataDIDDocVerificationMethodSchema), required=True
    )

    # The authentication method
    authentication = fields.List(
        fields.Nested(peopledataDIDDocAuthenticationSchema), required=True
    )

    # The service
    service = fields.List(fields.Nested(peopledataDIDDocServiceSchema), required=True)


class peopledataDIDResponseBody(BaseModel):
    """
    peopledata DID response body model
    """

    class Meta:

        # Schema class
        schema_class = "peopledataDIDResponseBodySchema"

    def __init__(
        self,
        *,
        did_doc: peopledataDIDDoc = None,
        version: str = None,
        status: str = None,
        **kwargs,
    ):
        """
        Initialize a peopledata DID response body model.

        Args:
            did_doc: The DIDDoc
            version: The version
        """
        super().__init__(**kwargs)

        # Set attributes
        self.did_doc = did_doc
        self.version = version
        self.status = status


class peopledataDIDResponseBodySchema(BaseModelSchema):
    """
    peopledata DID response body schema
    """

    class Meta:

        # Model class
        model_class = peopledataDIDResponseBody

        # Unknown fields are excluded
        unknown = EXCLUDE

    # The DIDDoc
    did_doc = fields.Nested(peopledataDIDDocSchema, required=True)

    # The version
    version = fields.Str(data_key="version")

    # The status
    status = fields.Str(data_key="status")
