  
import re
class RubyFormatter:
    outdentExp = [
        "^rescue\b", 
        "^ensure\b",
        "^elsif\b",
        "^end\b",
        "^else\b",
        "\bwhen\b",
        "^[^\{]*\}",
        "^[^\[]*\]"]
    indentExp = [
        "^module\b",
        "^class\b",
        "^if\b",
        "(=\s*|^)until\b",
        "(=\s*|^)for\b",
        "^unless\b",
        "(=\s*|^)while\b",
        "(=\s*|^)begin\b",
        "(^| )case\b",
        "\bthen\b",
        "^rescue\b",
        "^def\b",
        "\bdo\b",
        "^else\b",
        "^elsif\b",
        "^ensure\b",
        "\bwhen\b",
        "\{[^\}]*$",
        "\[[^\]]*$"]
    def __init__(self, file_string):
        self.file_string = file_string

    def run(self):
        return self.beautify(self.file_string)
    

    def rb_make_tab(self, tab):
        return "" if tab < 0 else " " * 3 * tab
    
    def rb_add_line(self, line, tab):
        line = line.rstrip().lstrip()
        line = self.rb_make_tab(tab) + line if len(line) > 0 else line
        return line

    def beautify(self, ugly):     
        comment_block = False
        in_here_doc = False
        here_doc_term = ""
        program_end = False
        multiLine_array = []
        multiLine_str = ""
        tline = ""
        tab = 0
        output = []  

        for line in ugly.splitlines(False):
            line = line.rstrip() #better strip begin and end

            if re.match("__END__$", line):
                program_end = True
            else:
                if((not re.match("\s*#", line)) and re.search("[^\\\]\\\s*$", line)):
                    multiLine_array.append(line)
                    multiLine_str += re.sub("^(.*)\\\s*$","\\1", line)
                    next
                if len(multiLine_str) > 0:
                  multiLine_array.append(line)
                  multiLine_str += re.sub("^(.*)\\\s*$","\\1", line)
                
                tline = (multiLine_str if len(multiLine_str) > 0 else line).lstrip()

                if re.match("=begin", tline):
                  comment_block = True
                if in_here_doc:
                    if re.search("\s*" + here_doc_term + "\s*", tline):
                        in_here_doc = False 
                else: 
                  if re.search("=\s*<<", tline):
                     here_doc_term = re.sub(".*=\s*<<-?\s*([_|\w]+).*","\\1", tline)
                     in_here_doc = len(here_doc_term) > 0
            
            if comment_block or program_end or in_here_doc:
                #add the line unchanged
                output.append(line)
            else:
                comment_line = re.match("^#", tline)
                if not comment_line:
                    #throw out sequences that lead to confusion
                    #todo
                    # delete end-of-line comments
                    tline = re.sub("#[^\"]+$","", tline)
                    # convert quotes
                    tline = re.sub("\\\"","'", tline)
                    
                    for oe in RubyFormatter.outdentExp:
                        if re.match(oe, tline):
                            tab -= 1
                            break
                if len(multiLine_array) > 0:
                    for ml in multiLine_array:
                        output.append(rb_add_line(ml, tab))
                    multiLine_array.clear
                    multiLine_str = ""
                else:
                    output.append(self.rb_add_line(line, tab))

                if not comment_line:
                    for ire in RubyFormatter.indentExp:
                        if re.search(ire, tline) and not re.search("\s+end\s*$", tline):
                            tab += 1
                            break
            if re.match("=end", tline):
                comment_block = False
        error = tab != 0
        if error:
            print "Error: indent/outdent mismatch: %d" %(tab)
        
        return ', '.join(output) + "\n" #, error
                 
               
