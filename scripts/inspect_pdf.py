from app.parsing.pdf_parser import extract_pages


PDF_PATH = "data/raw/sample.pdf"


def main():
    pages = extract_pages(PDF_PATH)

    print(f"Total pages: {len(pages)}")

    for page in pages:
        print("\n" + "=" * 80)
        print(f"PAGE {page.page_number}")
        print("=" * 80)
        print(page.text[:3000])


if __name__ == "__main__":
    main()