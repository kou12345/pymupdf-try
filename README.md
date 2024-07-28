# pymupdf-try

Describe your project here.

## PDF の markdown 化

`.venv/lib/python3.12/site-packages/pymupdf4llm/helpers/pymupdf_rag.py`

```
Traceback (most recent call last):
  File "/Users/user/workspace/pymupdf-try/src/main.py", line 17, in <module>
    md_text = pymupdf4llm.to_markdown(PDF_PATH)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/user/workspace/pymupdf-try/.venv/lib/python3.12/site-packages/pymupdf4llm/helpers/pymupdf_rag.py", line 763, in to_markdown
    page_output, images, tables, graphics = get_page_output(
                                            ^^^^^^^^^^^^^^^^
  File "/Users/user/workspace/pymupdf-try/.venv/lib/python3.12/site-packages/pymupdf4llm/helpers/pymupdf_rag.py", line 698, in get_page_output
    if is_significant(bbox, paths):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/user/workspace/pymupdf-try/.venv/lib/python3.12/site-packages/pymupdf4llm/helpers/pymupdf_rag.py", line 206, in is_significant
    points.extend([r.tl, r.tr, r.br, r.bl, r.tl])
                   ^^^^
AttributeError: 'Quad' object has no attribute 'tl'. Did you mean: 'll'?
```

上記のエラーが出るため`is_significant`を修正する

```python
def is_significant(box, paths):
    """Check whether the rectangle "box" contains 'signifiant' drawings.

    For this to be true, at least one path must cover an area,
    which is less than 90% of box. Otherwise we assume
    that the graphic is decoration (highlighting, border-only etc.).
    """
    box_area = abs(box) * 0.9  # 90% of area of box

    for p in paths:
        if p["rect"] not in box:
            continue
        if p["type"] == "f" and set([i[0] for i in p["items"]]) == {"re"}:
            # only borderless rectangles are contained: ignore this path
            continue
        points = []  # list of points represented by the items.
        # We are going to append all the points as they occur.
        for itm in p["items"]:
            if itm[0] in ("l", "c"):  # line or curve
                points.extend(itm[1:])  # append all the points
            elif itm[0] == "q":  # quad
                r = itm[1]
                # follow corners anti-clockwise
                points.extend([r.ll, r.ul, r.ur, r.lr, r.ll])
            else:  # rectangles come in two flavors.
                # starting point is always top-left
                r = itm[1]
                if isinstance(r, fitz.Quad):  # Check if it's a Quad object
                    if itm[-1] == 1:  # anti-clockwise (the standard)
                        points.extend([r.ll, r.ul, r.ur, r.lr, r.ll])
                    else:  # clockwise: area counts as negative
                        points.extend([r.ll, r.lr, r.ur, r.ul, r.ll])
                else:  # Assume it's a Rect object
                    if itm[-1] == 1:  # anti-clockwise (the standard)
                        points.extend([r.tl, r.bl, r.br, r.tr, r.tl])
                    else:  # clockwise: area counts as negative
                        points.extend([r.tl, r.tr, r.br, r.bl, r.tl])
        area = poly_area(points)  # compute area of polygon
        if area < box_area:  # less than threshold: graphic is significant
            return True
    return False
```
