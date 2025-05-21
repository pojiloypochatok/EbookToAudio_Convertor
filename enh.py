import torch

model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                  model='silero_te')

input_text = input('Enter input text\n')
apply_te(input_text, lan='en')