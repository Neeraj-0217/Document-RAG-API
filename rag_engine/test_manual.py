from rag_engine.pipeline import RAGPipeline

import os

pipeline = RAGPipeline()

script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(script_dir, "sample.pdf")

pipeline.ingest(pdf_path)
response = pipeline.query("What are the two project title mentioned in the document?")

print(response)

