import pymupdf4llm
import pathlib


PDF_PATH = ""

# テキストを取得する
# doc = pymupdf.open(PDF_PATH)  # open a document
# out = open("output.txt", "wb")  # create a text output
# for page in doc:  # iterate the document pages
#     text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
#     out.write(text)  # write text of page
#     out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
# out.close()


md_text = pymupdf4llm.to_markdown(PDF_PATH)

# now work with the markdown text, e.g. store as a UTF8-encoded file

pathlib.Path("output.md").write_bytes(md_text.encode())
