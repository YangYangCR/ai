import pypdfium2 as pdfium

if __name__ == "__main__":
    with open("demo1.pdf", "rb") as f:
        data = f.read()

    pdf = pdfium.PdfDocument(data)
    print(f"length is : {len(pdf)}")
    for page in pdf:
        print(f"page is : {page}")

    page = pdf[0]
    # scale 放大倍数  rotate 旋转
    bitmap = page.render(scale=2, rotation=0)
    print(f"bitmap is : {bitmap}")
    image = bitmap.to_pil()
    image.show()

    #获取页面尺寸
    width, height = pdf.get_page_size(0)
    print(f"width is : {width}")
    print(f"height is : {height}")

    # 元数据
    meta = pdf.get_metadata_dict()
    print(meta)