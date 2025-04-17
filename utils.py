import numpy as np
import torch
import tiktoken
from openai import OpenAI

client = OpenAI()

def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=[text], model=model)
    return torch.tensor(response.data[0].embedding)

def compute_mu(embedding):
    return torch.sigmoid(torch.tensor([torch.norm(embedding) % 1])).item()

def compute_variance(embedding):
    return embedding.var().item()

def compute_token_entropy(text, model="cl100k_base"):
    enc = tiktoken.get_encoding(model)
    tokens = enc.encode(text)
    counts = np.bincount(tokens)
    probs = counts / counts.sum()
    entropy = -np.sum([p * np.log(p) for p in probs if p > 0])
    return entropy / np.log(len(tokens) + 1e-9)

def generate_field(mu, entropy, var, grid_size=40):
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    Z = 1 / (1 + np.exp(-(np.sin(3*R) + np.cos(2*X)*np.sin(2*Y)) + 4 * (mu - 0.5) + 2 * (entropy - 0.5) + 3 * (var - 0.1)))
    return X, Y, Z
