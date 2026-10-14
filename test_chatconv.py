import json, unittest, chatconv
class T(unittest.TestCase):
    def setUp(self):
        with open("samples/chat.txt") as f: self.txt=f.read()
    def test_txt2jsonl(self):
        lines=chatconv.txt2jsonl(self.txt).splitlines()
        self.assertEqual(len(lines),2)
        m=json.loads(lines[0])["messages"]
        self.assertEqual(m[2],{"role":"user","content":"A list\nof two lines."})
    def test_roundtrip(self):
        j=chatconv.txt2jsonl(self.txt)
        self.assertEqual(chatconv.txt2jsonl(chatconv.jsonl2txt(j)),j)
    def test_bad_json(self):
        with self.assertRaises(SystemExit): chatconv.jsonl2txt("{bad")
    def test_skip_empty_chats(self):
        self.assertEqual(chatconv.txt2jsonl("notes only\n---\nUser: hi\n").count("\n"),1)
    def test_bad_record(self):
        with self.assertRaises(SystemExit) as e: chatconv.jsonl2txt('[1,2]')
        self.assertIn("expected", e.exception.code)
    def test_missing_file(self):
        with self.assertRaises(SystemExit) as e: chatconv.main(["txt2jsonl","nope.txt","out.jsonl"])
        self.assertIn("file not found", e.exception.code)
if __name__=="__main__": unittest.main(verbosity=2)
