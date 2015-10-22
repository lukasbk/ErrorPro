import unittest
import io
import parse

class ParserTestCase(unittest.TestCase):

    def test_parse(self):
        code = io.StringIO(
            "x = 12.5e-3 <0.001> [ms]\n" +
            "{\n" +
            "  a[m] b[N*s] #comment\n" +
            "  2.2  2.4e-1\n" +
            "  0.1\t0.2\n" +
            "}\n" +
            "$fit m*x1+b to (x1,x2) via m,b"
        )

        p = parse.parse_file(code)
        self.assertEqual(p[0].name, "x")
        self.assertEqual(p[0].value, "12.5e-3 ")
        self.assertEqual(p[0].uncertainty, "0.001")
        self.assertEqual(p[0].unit, "ms")
        self.assertEqual(p[1].header[0].name, "a")
        self.assertEqual(p[1].header[0].unit, "m")
        self.assertEqual(p[1].header[1].name, "b")
        self.assertEqual(p[1].header[1].unit, "N*s")
        self.assertEqual(p[1][0][0], "2.2")
        self.assertEqual(p[1][0][1], "2.4e-1")
        self.assertEqual(p[1][1][0], "0.1")
        self.assertEqual(p[1][1][1], "0.2")
        self.assertEqual(p[2].name, "fit")
        self.assertEqual(p[2], "m*x1+b to (x1,x2) via m,b")

if __name__ == '__main__':
    unittest.main()
