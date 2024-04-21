# https://discord.com/channels/1010980909568245801/1011105234820542554/1230930560956760185

import os
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
import torch
import torch.nn.functional as F
from torchvision import transforms
from torchvision.transforms.functional import crop
from tqdm.auto import tqdm
from transformers import AutoTokenizer, PretrainedConfig

import diffusers
from diffusers import (
    AutoencoderKL,
    DDPMScheduler,
    DiffusionPipeline,
    StableDiffusionXLPipeline,
    UNet2DConditionModel,
)
from diffusers.loaders import StableDiffusionXLLoraLoaderMixin
from diffusers.optimization import get_scheduler
from diffusers.utils import check_min_version, convert_state_dict_to_diffusers, convert_state_dict_to_kohya,  convert_all_state_dict_to_peft
from diffusers.utils.import_utils import is_xformers_available
from safetensors.torch import load_file, save_file
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA




def compute_distances(model_paths, text_dict, device="cuda"):
    results = {
        "Cosine": {},
        "Euclidean": {},
        "Manhattan": {},
        "Lengths": {},  # Store the lengths of embeddings here
        "Embeddings": {},
    }

    for model_path in model_paths:
        pipeline = StableDiffusionXLPipeline.from_single_file(os.path.join(r"I:\Stable Diffusion\Models\Stable-diffusion", model_path), use_safetensors=True)
        pipeline.to(device)
        tokenizer = pipeline.tokenizer_2
        text_encoder = pipeline.text_encoder_2


        # Extract text list for tokenization
        text_list = list(text_dict.values())

        # Tokenize the input text
        text_input_ids = tokenizer(
            text_list, truncation=True, padding="max_length", max_length=tokenizer.model_max_length, return_tensors="pt"
        ).input_ids.to(device)
        # tokens_one = tokenizers[0](
        #     captions, truncation=True, padding="max_length", max_length=tokenizers[0].model_max_length, return_tensors="pt"
        # ).input_ids 

        clip_skip = 2
        #enc_out = text_encoder(tokens, output_hidden_states=True, return_dict=True)

        prompt_embeds = text_encoder(
            text_input_ids.to(text_encoder.device),
            output_hidden_states=True,
        )

        pooled_prompt_embeds = prompt_embeds[0]
        
        clip_skip = 1
        prompt_embeds = prompt_embeds.hidden_states[-clip_skip]
        bs_embed, seq_len, _ = prompt_embeds.shape
        prompt_embeds = prompt_embeds.view(bs_embed, seq_len, -1)

        prompt_embeds = prompt_embeds.view(bs_embed, -1) # stack the sequences onto embeddings
        prompt_embeds = prompt_embeds / prompt_embeds.norm(dim=1, keepdim=True)

        
        # Compute cosine similarities
        
        cosine_similarities = torch.mm(prompt_embeds, prompt_embeds.T)

        # Compute Euclidean and Manhattan distances
        embeddings_np = prompt_embeds.cpu().numpy()
        euclidean_distances = distance_matrix(embeddings_np, embeddings_np)
        manhattan_distances = distance_matrix(embeddings_np, embeddings_np, p=1)

        # Store results
        model_name = os.path.basename(model_path)
        index_labels = list(text_dict.keys())
        results["Cosine"][model_name] = pd.DataFrame(cosine_similarities.cpu().numpy(), index=index_labels, columns=index_labels)
        results["Euclidean"][model_name] = pd.DataFrame(euclidean_distances, index=index_labels, columns=index_labels)
        results["Manhattan"][model_name] = pd.DataFrame(manhattan_distances, index=index_labels, columns=index_labels)
        #results["Lengths"][model_name] = embedding_lengths.cpu().numpy()
        results['Embeddings'][model_name] = embeddings_np

    return results


def print_results(results, decimals=3):
    for distance_type, models in results.items():
        print(f"{distance_type} Distances:")
        for model_name, df in models.items():
            print(f"\nModel: {model_name}")
            formatted_df = df.round(decimals)
            print(formatted_df)
        print("\n" + "-"*40)


def visualize_embeddings(embeddings_dict, text_dict, markers_dict, method='tsne', n_components=2, random_state=42):
    n_models = len(embeddings_dict)
    n_cols = 3  # Adjust based on how many columns you want in your subplot grid
    n_rows = (n_models + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 6, n_rows * 6))
    axes = axes.flatten()

    for idx, (model_name, embeddings) in enumerate(embeddings_dict.items()):
        if method == 'tsne':
            embeddings_reduced = TSNE(n_components=n_components, perplexity=min(len(embeddings) - 1, 30), random_state=random_state).fit_transform(embeddings)
        elif method == 'pca':
            pca = PCA(n_components=n_components, random_state=random_state)
            embeddings_reduced = pca.fit_transform(embeddings)
            # Capture the explained variance ratios for PCA1 and PCA2
            explained_var_ratio = pca.explained_variance_ratio_ * 100  # Convert to percentage
        else:
            raise ValueError("Method must be 'tsne' or 'pca'.")

        ax = axes[idx]
        scatter_plots = []
        for i, (label, text) in enumerate(text_dict.items()):
            marker = markers_dict.get(label, 'o')
            scatter = ax.scatter(embeddings_reduced[i, 0], embeddings_reduced[i, 1], label=text, marker=marker)
            scatter_plots.append(scatter)
        ax.set_title(f'{method.upper()} of {model_name}')

        if method == 'pca':
            # Set the axis labels with the explained variance
            ax.set_xlabel(f'PCA1 - {explained_var_ratio[0]:.2f}%')
            ax.set_ylabel(f'PCA2 - {explained_var_ratio[1]:.2f}%')

        # Only place the legend in the rightmost column plots
        if (idx + 1) % n_cols == 0:
            ax.legend(handles=scatter_plots, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1 if len(text_dict) <= 10 else 2)

    # Hide unused subplots
    for i in range(n_models, n_rows * n_cols):
        axes[i].axis('off')

    plt.tight_layout(pad=3.0)
    plt.subplots_adjust(right=0.8 if n_cols > 1 else 0.95)  # Adjust right edge to fit legends if multiple columns
    plt.show()



# Main setup
device = "cuda"
text_dict = {
    "DSS": "doggystyle sex", 
    "MSS": "missionary sex", 
    "RSC": "reverse_suspended_congress", 
    "MPS": "mating press", 
    "INT": "interracial",
    "FEL": "fellatio",
    "BLO": "blowjob",
    "ROS": "rough_sex",
    "CUM": "cum",
    "s1": "penis",
    "s2": "vagina",
    "s3": "anal",
    "s4": "oral",
    "POV": "pov",
    "SID": "side_view",
    "w1":"pineapple", 
    "w2":"pen",
    "w3":"dog", 
    "w4":"cat",
    "w5": "woman",
    "w6": "man",
    "w7": "1boy",
    "w8": "1girl",
    "w9": "landscape",
    "w10": "scenery",
    "w11": "love",
    "w12": "hairbow",
    "w13": "blonde",
    "w14": "ginger",
    "w15": "hair",
    "w16": "toes",
    "w17": "hero",
    "w18": "giant",
    "w19": "orgasm",
    "w20": "grape",
    "w21": "testicles",
    "t1": "photography",
    "t2": "anime",
    "g1":"beautiful", 
    "g2":"awe inspiring",
    "b1":"mutation", 
    "b2":"ugly",
}


markers_dict  = {
    "DSS": "x", 
    "MSS": "x", 
    "RSC": "x", 
    "MPS": "x", 
    "INT": "x",
    "FEL": "x",
    "BLO": "x",
    "CUM": "x",
    "t1":"s", 
    "t2":"s",
    "g1":"^", 
    "g2":"^",
    "b1":"v", 
    "b2":"v",
}

"""
'o': Circle
's': Square
'D': Diamond
'^': Triangle up
'v': Triangle down
'>': Triangle right
'<': Triangle left
'p': Pentagon
'+': Plus
'x': X
'.': Point
'*': Star
"""

model_paths = [
    r"sd_xl_base_1.0.safetensors",
    r"ponyDiffusionV6XL_v6StartWithThisOne.safetensors",
    r"animagineXLV31_v31.safetensors",
    r"juggernautXL_v8Rundiffusion.safetensors",
    r"mklanXXXNSFWVersion_mklan216XXX.safetensors"
]

with torch.no_grad():
    # Compute distances
    results = compute_distances(model_paths, text_dict)

    # Print results organized by distance type, then by model
    print_results(results)


visualize_embeddings(results['Embeddings'], text_dict, markers_dict, method='pca')
#visualize_embeddings(results['Embeddings'], text_dict, markers_dict, method='tsne')

