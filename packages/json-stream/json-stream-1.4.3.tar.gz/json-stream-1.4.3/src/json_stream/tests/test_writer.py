import json
from io import StringIO
from time import sleep
from unittest import TestCase

from json_stream.writer import StreamableDict, StreamableList


class TestWriter(TestCase):
    def test_writer(self):
        def dict_content(n):
            yield "a  list", range(4)

        o = StreamableDict(dict_content(5))

        buffer = StringIO()
        json.dump(o, buffer)
        self.assertEqual('{"a  list": [0, 1, 2, 3]}', buffer.getvalue())
