"""DID peopledata class and resolver methods."""

from peopledata_did.v1_0.utils.diddoc import DIDDoc
from peopledata_did.v1_0.utils.wallet.crypto import ed25519_pk_to_curve25519
from peopledata_did.v1_0.utils.wallet.key_type import KeyType
from peopledata_did.v1_0.utils.wallet.util import b58_to_bytes, bytes_to_b58


class DIDpeopledata:
    """DID peopledata parser and resolver."""

    _key_type: KeyType
    _public_key: bytes

    def __init__(self, public_key: bytes, key_type: KeyType) -> None:
        """Initialize new DIDpeopledata instance."""
        self._public_key = public_key
        self._key_type = key_type

    @classmethod
    def from_public_key(cls, public_key: bytes, key_type: KeyType) -> "DIDpeopledata":
        """Initialize new DIDpeopledata instance from public key and key type."""

        return cls(public_key, key_type)

    @classmethod
    def from_public_key_b58(cls, public_key: str, key_type: KeyType) -> "DIDpeopledata":
        """Initialize new DIDpeopledata instance from base58 encoded public key and key type."""
        public_key_bytes = b58_to_bytes(public_key)
        return cls.from_public_key(public_key_bytes, key_type)

    @classmethod
    def from_fingerprint(cls, fingerprint: str) -> "DIDpeopledata":
        """Initialize new DIDpeopledata instance from multibase encoded fingerprint.

        The fingerprint contains both the public key and key type.
        """
        # Assert fingerprint is in multibase format
        assert fingerprint[0] == "z"

        # Get key bytes, remove multicodec prefix
        key_bytes_with_prefix = b58_to_bytes(fingerprint[1:])

        # Get associated key type with prefixed bytes
        key_type = KeyType.from_prefixed_bytes(key_bytes_with_prefix)

        if not key_type:
            raise Exception(
                f"No key type for prefixed public key '{key_bytes_with_prefix}' found."
            )

        # Remove the prefix bytes to get the public key
        prefix_len = len(key_type.multicodec_prefix)
        public_key_bytes = key_bytes_with_prefix[prefix_len:]

        return cls(public_key_bytes, key_type)

    @classmethod
    def from_did(cls, did: str) -> "DIDpeopledata":
        """Initialize a new DIDpeopledata instance from a fully qualified did:peopledata string.

        Extracts the fingerprint from the did:peopledata and uses that to constrcut the did:peopledata.
        """
        did_parts = did.split("#")
        _, fingerprint = did_parts[0].split("did:peopledata:")

        return cls.from_fingerprint(fingerprint)

    @property
    def prefixed_public_key(self) -> bytes:
        """Getter for multicodec prefixed public key."""
        return b"".join([self.key_type.multicodec_prefix, self.public_key])

    @property
    def fingerprint(self) -> str:
        """Getter for DID peopledata fingerprint."""
        return f"z{bytes_to_b58(self.prefixed_public_key)}"

    @property
    def did(self) -> str:
        """Getter for full did:peopledata string."""
        return f"did:peopledata:{self.fingerprint}"

    @property
    def did_doc(self) -> dict:
        """Getter for did document associated with did:peopledata."""
        resolver = DID_KEY_RESOLVERS[self.key_type]
        return resolver(self)

    @property
    def public_key(self) -> bytes:
        """Getter for public key."""
        return self._public_key

    @property
    def public_key_b58(self) -> str:
        """Getter for base58 encoded public key."""
        return bytes_to_b58(self.public_key)

    @property
    def key_type(self) -> KeyType:
        """Getter for key type."""
        return self._key_type

    @property
    def key_id(self) -> str:
        """Getter for key id."""
        return f"{self.did}#{self.fingerprint}"


def construct_did_key_ed25519(did_key: "DIDpeopledata") -> dict:
    """Construct Ed25519 did:peopledata.

    Args:
        did_key (DIDpeopledata): DID peopledata instance to parse ed25519 did:peopledata document from

    Returns:
        dict: The ed25519 did:peopledata did document

    """
    curve25519 = ed25519_pk_to_curve25519(did_key.public_key)
    x25519 = DIDpeopledata.from_public_key(curve25519, KeyType.X25519)

    did_doc = construct_did_signature_key_base(
        id=did_key.did,
        key_id=did_key.key_id,
        verification_method={
            "id": did_key.key_id,
            "type": "Ed25519VerificationKey2018",
            "controller": did_key.did,
            "publicKeyBase58": did_key.public_key_b58,
        },
    )

    # Ed25519 has pair with X25519
    did_doc["keyAgreement"].append(
        {
            "id": f"{did_key.did}#{x25519.fingerprint}",
            "type": "X25519KeyAgreementKey2019",
            "controller": did_key.did,
            "publicKeyBase58": bytes_to_b58(curve25519),
        }
    )

    return did_doc


def construct_did_signature_key_base(
    *, id: str, key_id: str, verification_method: dict
):
    """Create base DID peopledata structure to use for most signature keys.

    May not be suitable for all DID peopledata types

    """

    return {
        "@context": DIDDoc.CONTEXT,
        "id": id,
        "verificationMethod": [verification_method],
        "authentication": [key_id],
        "assertionMethod": [key_id],
        "capabilityDelegation": [key_id],
        "capabilityInvocation": [key_id],
        "keyAgreement": [],
    }


DID_KEY_RESOLVERS = {
    KeyType.ED25519: construct_did_key_ed25519,
}
