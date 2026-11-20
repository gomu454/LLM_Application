from retrieval import load_chunks


chunks = load_chunks()
print("문단 수:",len(chunks))


for chunk in chunks[:3]:
    # print(chunk["source"], chunk["text"][:60])
    print(f"파일명 : {chunk['source']}")
    print(f"내용 : {chunk['text'][:60]}\n")

# 실행명령은 Python 파일이 아닌 터미널에 입력:
# .\.venv\Scripts\python.exe backend/check_chunks.py

def make_words(text):
    cleaned = text.lower()
    for mark in "?!,./:()-":
        cleaned = cleaned.replace(mark,"")
        return cleaned.split()


def find_chunks(question):

    question_words = make_words(question)
    found = []
    for chunk in load_chunks():
        content_words = make_words(chunk["text"])
        for word in question_words:
            if len(word) > 1 and word in content_words:
                found.append(chunk)
                break
        if len(found) == 3:
            break
    return found
