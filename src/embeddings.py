from langchain.embeddings import FastEmbedEmbeddings


def get_embeddings():
    """
    Load and return FastEmbed embeddings (CPU-only, production safe).
    """
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
