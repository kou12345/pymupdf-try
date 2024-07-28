import pymupdf

PDF_PATH = "/Users/kou12345/Downloads/コンピュータアーキテクチャのエッセンス 第2版.pdf"

# テキストを取得する
doc = pymupdf.open(PDF_PATH)  # open a document
out = open("output.txt", "wb")  # create a text output
for page in doc:  # iterate the document pages
    text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
    out.write(text)  # write text of page
    out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
out.close()
