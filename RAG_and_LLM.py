from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import pathlib
from nltk.tokenize import word_tokenize
import os
from function_defintions import BreakDown, Search_with_custom_alpha
from langchain_groq import ChatGroq

load_dotenv()
os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.2-90b-vision-preview",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

root_dir = pathlib.Path(__file__).parent
folder_path=str(root_dir /'textbooks'/'en' )

def scraper():
    documents = []
    doc_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                documents.append(file.read())
                doc_names.append(filename)
    chunks=BreakDown(documents)                        
    tokenized_corpus = [word_tokenize(chunk.lower()) for chunk in chunks]
    return chunks,tokenized_corpus

template_for_rag = """
query: {query}
Context: {retrieved_info}
You are a Medical Expert tasked with selecting the correct answer for the MCQ based on the given context. 
If there is no relevant context regarding the given query then output Question cannot be solved with current database. I need to study more, Please give me the relevant Information. 
Give a systematic step by step explanation why the answer provided is correct.
"""
rag_prompt = PromptTemplate(
input_variables=["retrieved_info", "query"],
template=template_for_rag
)

chain=LLMChain(llm=llm,prompt=rag_prompt,output_key="RAG_info")

chunks,tokenized_corpus= scraper()

def Brief_Description(query,best_n=10,alpha=0.5):
    retrieved_info=Search_with_custom_alpha(query,chunks,tokenized_corpus,best_n,alpha)
    response = chain.invoke({
    "retrieved_info":retrieved_info ,
    "query": query
})
    return response.get("RAG_info")

def Composer(query, options, hs_result, rag_result ):
    prompt = f"""
    Question: {query}
    rag_result is a concise one, hs_result is a detailed one.
    Search for neccesary information from Both.
    Context from retrieved information: {hs_result} and {rag_result} 
    Search for neccesary information from Both.
    You are a Medical Expert tasked with selecting the correct answer for the MCQ based on the given context. 
    Please answer the Question based on the context from retrieved information provided above.
    If you can not find the exact answers. You need to understand and pick up the most related options.
    If {rag_result} says something like If there is no relevant context regarding the given query then output Question cannot be solved with current database. I need to study more, Please give me the relevant Information. Output same as {rag_result}.
    Choose the correct option based on the context:
    Options:
    A: {options['A']}
    B: {options['B']}
    C: {options['C']}
    D: {options['D']}
    
    **Please respond with the letter corresponding to the correct answer (A, B, C, or D).
    Do not provide any explanation, just the letter.**
    """
    quiz_prompt = PromptTemplate(
    input_variables=["query", "rag_result", "option_a", "option_b", "option_c", "option_d", "hs_result"],
    template=prompt
)
    chain1 = LLMChain(
    llm=llm,
    prompt=quiz_prompt,
    output_key="Final_answer"
)
    response = chain1.invoke({
        "query": query,
        "rag_result": rag_result,
        "option_a": options['A'],
        "option_b": options['B'],
        "option_c": options['C'],
        "option_d": options['D'], 
        "hs_result" : hs_result

    })
    print (f"Options: {response.get("Final_answer")}")
    print(f"Brief Description: {rag_result}")
    return response.get("Final_answer")

def MCQSolver(query, options, best_n=10, alpha=0.5):
    hs_result = Search_with_custom_alpha(query,chunks,tokenized_corpus,best_n,alpha)
    rag_result = Brief_Description(query, best_n, alpha)
    return Composer(query, options, hs_result, rag_result )



# test = {"question": "A 59-year-old woman with stage IV lung cancer comes to the physician because of progressively worsening weakness in the past 3 months. She has had a 10.5-kg (23-lb) weight loss during this period. Her BMI is 16 kg/m2. She appears thin and has bilateral temporal wasting. Which of the following is the most likely primary mechanism underlying this woman's temporal muscle atrophy?", "answer": "Proteasomal degradation of ubiquitinated proteins", "options": {"A": "Cytochrome c-mediated activation of proteases", "B": "Lipase-mediated degradation of triglycerides", "C": "TNF-α-mediated activation of caspases", "D": "Proteasomal degradation of ubiquitinated proteins"}, "meta_info": "step1", "answer_idx": "D", "metamap_phrases": ["59 year old woman", "stage IV lung cancer", "physician", "worsening weakness", "past 3 months", "a 10 kg", "23", "weight loss", "period", "BMI", "kg/m2", "appears thin", "bilateral temporal wasting", "following", "most likely primary mechanism", "woman's temporal"]}
# query = test["question"]
# options = test["options"]

# print(MCQSolver(query, options, 10, 0.3))