import os
import fitz  # PyMuPDF
import docx

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    all_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text().strip()
        if text:
            all_text.append(text)

    return "\n".join(all_text)

def load_documents(folder_path="docs"):
    documents = []

    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        ext = filename.lower().split(".")[-1]

        try:
            if ext == "txt":
                text = extract_text_from_txt(path)
            elif ext == "docx":
                text = extract_text_from_docx(path)
            elif ext == "pdf":
                text = extract_text_from_pdf(path)
            else:
                print(f"Unsupported file type: {filename}")
                continue

            documents.append({
                "filename": filename,
                "text": text
            })

            print(f"✅ Loaded: {filename}")

        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")

    return documents

if __name__ == "__main__":
    docs = load_documents()
    print(f"\n📄 Total documents loaded: {len(docs)}\n")

    for doc in docs:
        print(f"📘 {doc['filename']}")
        words = doc['text'].split()
        preview = " ".join(words[:100])
        print(f"📝 First 100 words:\n{preview}\n{'-'*80}")
