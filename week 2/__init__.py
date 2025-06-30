from fastembed import TextEmbedding
from qdrant_client import QdrantClient

from helpers import create_base, search


MODEL_NAME = "jinaai/jina-embeddings-v2-small-en"

documents = [
    {
        "text": "Yes, even if you don't register, you're still eligible to submit the homeworks.\nBe aware, however, that there will be deadlines for turning in the final projects. So don't leave everything for the last minute.",
        "section": "General course-related questions",
        "question": "Course - Can I still join the course after the start date?",
        "course": "data-engineering-zoomcamp",
    },
    {
        "text": "Yes, we will keep all the materials after the course finishes, so you can follow the course at your own pace after it finishes.\nYou can also continue looking at the homeworks and continue preparing for the next cohort. I guess you can also start working on your final capstone project.",
        "section": "General course-related questions",
        "question": "Course - Can I follow the course after it finishes?",
        "course": "data-engineering-zoomcamp",
    },
    {
        "text": "The purpose of this document is to capture frequently asked technical questions\nThe exact day and hour of the course will be 15th Jan 2024 at 17h00. The course will start with the first  “Office Hours'' live.1\nSubscribe to course public Google Calendar (it works from Desktop only).\nRegister before the course starts using this link.\nJoin the course Telegram channel with announcements.\nDon’t forget to register in DataTalks.Club's Slack and join the channel.",
        "section": "General course-related questions",
        "question": "Course - When will the course start?",
        "course": "data-engineering-zoomcamp",
    },
    {
        "text": "You can start by installing and setting up all the dependencies and requirements:\nGoogle cloud account\nGoogle Cloud SDK\nPython 3 (installed with Anaconda)\nTerraform\nGit\nLook over the prerequisites and syllabus to see if you are comfortable with these subjects.",
        "section": "General course-related questions",
        "question": "Course - What can I do before the course starts?",
        "course": "data-engineering-zoomcamp",
    },
    {
        "text": "Star the repo! Share it with friends if you find it useful ❣️\nCreate a PR if you see you can improve the text or the structure of the repository.",
        "section": "General course-related questions",
        "question": "How can we contribute to the course?",
        "course": "data-engineering-zoomcamp",
    },
]


# Q1
query = "I just discovered the course. Can I join now?"

embedding_model = TextEmbedding(MODEL_NAME)
query_vector = list(embedding_model.embed([query]))
print(f"A1: {min(query_vector[0])}")

# Q2
doc = "Can I still join the course after the start date?"

doc_vector = list(embedding_model.embed([doc]))
print(f"A2: {query_vector[0].dot(doc_vector[0])}")

# Q3
documents_vector = list(embedding_model.embed([x["text"] for x in documents]))
max_similarity = -1
max_similarity_doc_id = None

for idx, dv in enumerate(documents_vector):
    similarity = query_vector[0].dot(dv)
    if similarity < max_similarity:
        continue
    max_similarity = similarity
    max_similarity_doc_id = idx


print(f"A3: {max_similarity_doc_id}")

# Q4
documents_extanded_vector = list(
    embedding_model.embed([f"{x['question']} {x['text']}" for x in documents])
)
max_similarity = -1
max_similarity_doc_id = None

for idx, dv in enumerate(documents_extanded_vector):
    similarity = query_vector[0].dot(dv)
    if similarity < max_similarity:
        continue
    max_similarity = similarity
    max_similarity_doc_id = idx

print(f"A4: {max_similarity_doc_id}")

# Q5

# info from https://qdrant.github.io/fastembed/examples/Supported_Models/
print("A5: 384")

# Q6

client = QdrantClient(url="http://localhost:6333")
collection_name = "homework-2"
create_base(client, collection_name)
result = search(client, collection_name, query)
print(f"A6: {result.score}")
