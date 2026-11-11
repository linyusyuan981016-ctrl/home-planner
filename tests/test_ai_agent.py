"""Tests for the local Ollama assistant client."""

import io
import json
import unittest
from unittest.mock import patch

from home_planner.models import Home
from home_planner.services.ai_agent import stream_assistant


class TestOllamaAssistant(unittest.TestCase):
    @patch("home_planner.services.ai_agent.urlopen")
    def test_streams_response_chunks_without_output_cap(self, mocked_urlopen):
        chunks = [
            {"message": {"content": "Place "}, "done": False},
            {"message": {"content": "furniture thoughtfully."}, "done": True},
        ]
        response_body = b"".join(
            json.dumps(chunk).encode("utf-8") + b"\n" for chunk in chunks
        )
        mocked_urlopen.return_value.__enter__.return_value = io.BytesIO(response_body)

        answer = "".join(
            stream_assistant(
                [{"role": "user", "content": "Suggest an improvement."}],
                home=Home(name="Test home"),
                furniture=[],
            )
        )

        self.assertEqual(answer, "Place furniture thoughtfully.")
        request = mocked_urlopen.call_args.args[0]
        payload = json.loads(request.data)
        self.assertTrue(payload["stream"])
        self.assertNotIn("num_predict", payload["options"])
        self.assertEqual(mocked_urlopen.call_args.kwargs["timeout"], 60)


if __name__ == "__main__":
    unittest.main()