import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def create_vectorstore(text, embeddings, persist_dir):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])
    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_dir)
    return vectordb

def get_custom_rag_chain(llm, vectordb):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
            You are a helpful assistant that answers questions using ONLY the given context.

            Always:
            - Respond in the same language as the user's question (Telugu, English, or mixed).
            - If the user uses English words but means Telugu (code-mixed), answer accordingly.
            - Be concise, accurate, and contextual.

            Context:
            {context}

            Question:
            {question}

            Answer:"""
                )
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt)

    def ask(query):
        docs = retriever.get_relevant_documents(query)
        return qa_chain.run(input_documents=docs, question=query)

    return ask
