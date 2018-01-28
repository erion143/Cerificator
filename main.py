import shelve as sh
import subprocess as sp
import os


MS_WORD = r'C:\Program Files (x86)\Microsoft Office\Office12\winword.exe'


def open_batch(cur_class, batch):
    with sh.open(cur_class.name) as store:
        assert batch in store
        return cur_class(store[batch])


def print_docx(_filename):
    if os.path.splitext(_filename)[-1] in ('.doc', '.docx'):
        sp.Popen([MS_WORD,
                  _filename,
                  "/mFilePrintDefault",
                  "/mFileExit"]).communicate()

