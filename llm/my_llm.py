from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    load_index_from_storage,
)
from llama_index.vector_stores import SupabaseVectorStore
# set_global_service_context

from llama_index.storage.storage_context import StorageContext
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores import SimpleVectorStore
from llama_index.storage.index_store import SimpleIndexStore

from llama_index.llms import LlamaCPP, HuggingFaceLLM
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from llama_index.prompts import PromptTemplate

# from llama_index.vector_stores import PineconeVectorStore

# api_key = ""
# environment = """
# index_name = ""

model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"


def get_llm():

    llm = LlamaCPP(
        # You can pass in the URL to a GGML model to download it automatically
        # model_url=model_url,
        # optionally, you can set the path to a pre-downloaded model instead of model_url
        model_path="llama-2-13b-chat.Q4_0.gguf",
        temperature=0.1,
        max_new_tokens=2048,
        # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
        context_window=3900,
        # kwargs to pass to __call__()
        generate_kwargs={},
        # kwargs to pass to __init__()
        # set to at least 1 to use GPU
        model_kwargs={"n_gpu_layers": 23},  #20-24 layers works best on my setup.
        # transform inputs into Llama2 format
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=True,
    )

    # llm = HuggingFaceLLM(
    #     model_name="zephyr-7b-beta.Q4_K_M.gguf",
    #     tokenizer_name="zephyr-7b-beta.Q4_K_M.gguf",
    #     query_wrapper_prompt=PromptTemplate("<|system|>\n</s>\n<|user|>\n{query_str}</s>\n<|assistant|>\n"),
    #     context_window=3900,
    #     max_new_tokens=2048,
    #     model_kwargs={},
    #     # tokenizer_kwargs={},
    #     generate_kwargs={"temperature": 0.7, "top_k": 50, "top_p": 0.95},
    #     messages_to_prompt=messages_to_prompt,
    #     device_map="auto",
    # )

    return llm


def get_query_engine(llm, filename):
    # use Huggingface embeddings

    print("-----LOGGING----- start query_engine")
    embed_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    # create a service context
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )

    # set_global_service_context(service_context)

    # # load documents
    documents = SimpleDirectoryReader(
        input_files = [f"./docs/{filename}"]
    ).load_data()

    # documents = SimpleDirectoryReader("./test_docs").load_data()
    
    # # create vector store index
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    print("-----LOGGING----- generated index:",index)

    # index.storage_context.persist("./test_indexcache_one/")
    # print("-----LOGGING----- persisted index")

    # set up query engine
    query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=1
    )
    return query_engine

def get_query_engine_from_cache(llm,filename):

    print("-----LOGGING----- start qengine_cache")

    embed_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    # create a service context
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )

    # storage_context = StorageContext.from_defaults(
    #     docstore=SimpleDocumentStore.from_persist_dir(persist_dir = f"./indexcache/{filename}"),
    #     vector_store=SimpleVectorStore.from_persist_dir(persist_dir = f"./indexcache/{filename}"),
    #     index_store=SimpleIndexStore.from_persist_dir(persist_dir = f"./indexcache/{filename}"),
    # )

    storage_context = StorageContext.from_defaults(persist_dir=f"./indexcache/{filename}")

    print("-----LOGGING----- loading index from cache as new_index")

    # new_index = load_index_from_storage(storage_context)

    new_index = load_index_from_storage(storage_context, service_context=service_context)
    
    print("-----LOGGING----- loaded new_index done", new_index)

    query_engine = new_index.as_query_engine(
        streaming=True,
        similarity_top_k=1
    )

    print("-----LOGGING----- after query_engine")

    return query_engine

def get_query_engine_supabase(llm, filename):
    # use Huggingface embeddings

    print("-----LOGGING----- start query_engine - SUPABASE")
    embed_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    # create a service context
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )

    # set_global_service_context(service_context)

    # # load documents
    documents = SimpleDirectoryReader(
        input_files = [f"./docs/{filename}"]
    ).load_data()

    DB_CONNECTION = ""

    print("-----LOGGING----- initializing vector_store")

    vector_store = SupabaseVectorStore(
        postgres_connection_string=DB_CONNECTION, 
        collection_name='reviewIndexes',
        dimension='768',
    )
    print("-----LOGGING----- initialized vector_store")

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    print("-----LOGGING----- initialized storage_context")

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)

    print("-----LOGGING----- generated index:",index)

    # set up query engine
    query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=1
    )
    return query_engine