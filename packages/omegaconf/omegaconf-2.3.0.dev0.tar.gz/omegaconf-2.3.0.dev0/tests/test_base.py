from typing import Any, Optional

from pytest import mark, param

from omegaconf.base import Metadata


class TestMetadata:
    @mark.parametrize(
        "optional, expected",
        [
            param(True, Optional[int], id="True"),
            param(False, int, id="False"),
        ],
    )
    def test_type_hint_getter(self, optional: bool, expected: Any) -> None:
        metadata = Metadata(int, "object_type", optional, "key")
        assert metadata.type_hint == expected
