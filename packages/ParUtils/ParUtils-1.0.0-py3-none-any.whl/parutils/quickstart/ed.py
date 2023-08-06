"""
This script extracts all Python doc ('# comments included) present in the
'in_dir' directories and subdirectories (recursive search).
This can be useful for spell checking.
"""

import parutils.quickstart as qs
from parutils.ed import extract_doc

in_dirs = [qs.quickstart_dir]
out_path = 'extract_doc_out.txt'

extract_doc(in_dirs, out_path)
