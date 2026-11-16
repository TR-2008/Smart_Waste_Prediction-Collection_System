# Community Waste Collection and Sorting Assistant

All required data is supplied. Do not collect observations, write survey comments, photograph objects, or label images.

1. Open Start_Here_Colab.ipynb in free Google Colab.
2. Upload the complete AI_for_Everyone_Ready_Datasets.zip when the notebook asks for it.
3. Run the loading cells. The matching Word proposal explains the modelling and app tasks.

main.csv contains 1000 complete records and a fixed split column. Use only the named input features in meta.json; record_id, split, and the target are not model inputs.

feedback.csv contains 30 authored English examples and supplied sentiment_label values. These are reference labels for evaluation, not real customer or student comments.

images.npz contains x_train, y_train, x_validation, y_validation, x_test, and y_test. The input arrays are already sized and have values from 0 to 255. Load with numpy.load(..., allow_pickle=False). Keep the given splits and class order in meta.json.

The supplied nltk_data/sentiment/vader_lexicon.zip allows NLTK sentiment analysis without downloading data at app startup. The sample_images folder provides images for a live demonstration. Prompt test cases are fixed classroom exercises, not model results.

No paid API, GPU plan, database, domain, or cloud hosting subscription is required. Optional Groq calls must use its Free Plan only. When a free quota is unavailable, the app uses a clearly labelled offline Python summary. The instructor's paid ChatGPT or Claude access is for coding and prompt assistance, not a paid API integration.

Keep full image arrays for training in Colab or on your own computer. Publish app.py, small model files, small CSV files, matching package versions, and attribution on GitHub. Use free Streamlit Community Cloud to run the Python app from that repository.
