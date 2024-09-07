# LegalSummerizer

You can upload PDF, Word Docs, Text, and Images of legal Documents, it gives summaries of them.

I used a Pre-Trained model called Longformer Encoder-Decoder (LED), it's variant "allenai/led-base-16384" 

The "allenai/led-base-16384" model is pre-trained on the CNN/Daily Mail dataset for document summarization. This dataset consists of news articles and their corresponding summaries. The model learns to condense long news articles into concise summaries.

I Fine-tuned this model on a large dataset of 250000 legal judgments and their summaries.

I have deployed this in Streamlit, you can access it here.
https://legalsummerizer-vgbxty4ryy8z85tk2lucnx.streamlit.app/
