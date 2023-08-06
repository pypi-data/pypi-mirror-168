import re

from marshmallow.validate import Regexp

peopledata_DID_REGEX = (
    "did:peopledata(:?(?P<did_type>0|1|2|3|4))?:(?P<identifier>z[a-km-zA-HJ-NP-Z1-9]+)"
)
peopledata_DID_PATTERN = re.compile(f"^{peopledata_DID_REGEX}$")


class peopledataDID(Regexp):
    """Validate value against peopledata DID."""

    EXAMPLE = "z6MkfiSdYhnLnS6jfwSf2yS2CiwwjZGmFUFL5QbyL2Xu8z2E"
    PATTERN = rf"^did:peopledata(:?(?P<did_type>0|1|2|3|4))?:(?P<identifier>z[a-km-zA-HJ-NP-Z1-9]+)"

    def __init__(self):
        """Initializer."""

        super().__init__(
            peopledataDID.PATTERN,
            error="Value {input} is not an peopledata decentralized identifier (DID)",
        )


peopledata_DID = {"validate": peopledataDID(), "example": peopledataDID.EXAMPLE}


if __name__ == "__main__":
    print(
        peopledata_DID_PATTERN.match(
            "did:peopledata:0:z6MkfiSdYhnLnS6jfwSf2yS2CiwwjZGmFUFL5QbyL2Xu8z2E"
        ).group("did_type")
    )
    print(
        peopledata_DID_PATTERN.match(
            "did:peopledata:z6MkfiSdYhnLnS6jfwSf2yS2CiwwjZGmFUFL5QbyL2Xu8z2E"
        ).group("did_type")
    )
