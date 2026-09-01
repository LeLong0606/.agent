"""Kiểm thử công cụ audit localization key."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "audit_localization_keys.py"
SPEC = importlib.util.spec_from_file_location("audit_localization_keys", SCRIPT_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AuditLocalizationKeysTests(unittest.TestCase):
    """Xác nhận quy tắc tìm kiếm và chuyển đổi raw localization key."""

    def test_to_identifier_matches_csharp_generator(self) -> None:
        self.assertEqual("ReactMessageSuccess", MODULE.to_identifier("REACT_MESSAGE_SUCCESS"))
        self.assertEqual("LogRedisPubsubError", MODULE.to_identifier("LOG_REDIS_PUBSUB_ERROR"))

    def test_scan_and_fix_raw_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_path = Path(temporary_directory) / "Controller.cs"
            source_path.write_text(
                "using Microsoft.Extensions.Localization;\n\n"
                "var message = _localizer[\"REACT_MESSAGE_SUCCESS\"];\n",
                encoding="utf-8",
            )
            identifiers = {"REACT_MESSAGE_SUCCESS": "ReactMessageSuccess"}

            findings = MODULE.scan_file("BridgeChat.MessageService", source_path, identifiers)
            fixed_count = MODULE.fix_file(source_path, identifiers)
            updated_source = source_path.read_text(encoding="utf-8")

            self.assertEqual(1, len(findings))
            self.assertEqual(1, fixed_count)
            self.assertIn("using BridgeChat.SharedLibraries.Core.Localization;", updated_source)
            self.assertIn("_localizer[LocalizationKeys.ReactMessageSuccess]", updated_source)
            self.assertNotIn('"REACT_MESSAGE_SUCCESS"', updated_source)

    def test_scan_plain_localizer_parameter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source_path = Path(temporary_directory) / "Validator.cs"
            source_path.write_text(
                'var message = localizer["VALIDATION_SENDER_ID_EMPTY"];\n',
                encoding="utf-8",
            )
            identifiers = {"VALIDATION_SENDER_ID_EMPTY": "ValidationSenderIdEmpty"}

            findings = MODULE.scan_file("BridgeChat.MessageService", source_path, identifiers)

            self.assertEqual(1, len(findings))
            self.assertEqual("ValidationSenderIdEmpty", findings[0].identifier)


if __name__ == "__main__":
    unittest.main()
