import requests

from qdrant_client import models

DATA_URL = "https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json"
MODEL_NAME = "BAAI/bge-small-en"
MODEL_DIM = 384


def _download_data(url):
    docs_url = url
    docs_response = requests.get(docs_url)
    documents_raw = docs_response.json()

    documents = []

    for course in documents_raw:
        course_name = course["course"]
        if course_name != "machine-learning-zoomcamp":
            continue

        for doc in course["documents"]:
            doc["course"] = course_name
            documents.append(doc)

    return documents


def _create_collection(client, collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=MODEL_DIM, distance=models.Distance.COSINE
        ),
    )


def _upload_collection(client, collection_name, documents):
    data_points = []
    for idx, document in enumerate(documents):
        point = models.PointStruct(
            id=idx,
            vector=models.Document(
                text=f"{document['question']} {document['text']}",
                model=MODEL_NAME,
            ),
            payload={
                "text": document["text"],
                "course": document["course"],
                "section": document["section"],
                "question": document["question"],
            },
        )
        data_points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=data_points,
    )


def search(client, collection, query, limit=1):
    results = list(
        client.query_points(
            collection_name=collection,
            query=models.Document(text=query, model=MODEL_NAME),
            limit=limit,
            with_payload=True,
        )
    )
    return results[0][1][0]


def create_base(client, collection_name):
    _create_collection(client, collection_name)
    _upload_collection(client, collection_name, _download_data(DATA_URL))
