import nltk
from nltk.tokenize import sent_tokenize

class TextSplitter():
    def __init__(self, max_chunk_length=1500):
        self.max_chunk_length = max_chunk_length

    def process(self, text):
        sentences = sent_tokenize(text)
        chunks = self._split_into_chunks(sentences)
        return chunks

    def _split_into_chunks(self, sentences):
        chunks = []
        chunk = ''
        for sentence in sentences:
            if len(chunk) + len(sentence) <= self.max_chunk_length:
                chunk += sentence + ' '
            else:
                chunks.append(chunk.strip())
                chunk = sentence + ' '
        if chunk:
            chunks.append(chunk.strip())  # Add the last chunk
        return chunks
