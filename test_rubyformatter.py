import unittest, rubyformatter

class TestRubyFormatter(unittest.TestCase):

    def assert_output(self, input, expected_output):
        rf = rubyformatter.RubyFormatter(input)
        self.assertEqual(expected_output, rf.run)

    def test_one_comment_line(self):
        cl = "# my comment line"
        self.assert_output(cl, cl)
    
    def test_simple_class(self):
        klass = """
        class Bar
        end
        """
        self.assert_outpu(klass, klass)

    def test_simple_format(self):
        pre = """
        class Foo
          def bar
            end
            end
        """
        formatted = """
        class Foo
          def bar
          end
        end
        """
        self.assert_output(pre, formatted)
        

if __name__ == "__main__":
    unittest.main() 
