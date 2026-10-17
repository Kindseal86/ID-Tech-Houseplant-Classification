{
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 666
        },
        "id": "03wR1Ktf-kbS",
        "outputId": "16f453ac-6b2f-4a20-d203-19d8e08b8a2e"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: biopython in /usr/local/lib/python3.13/dist-packages (1.88)\n",
            "Requirement already satisfied: numpy in /usr/local/lib/python3.13/dist-packages (from biopython) (2.1.3)\n",
            "Colab notebook detected. This cell will run indefinitely so that you can see errors and logs. To turn off, set debug=False in launch().\n",
            "* Running on public URL: https://b160c7131b34fd04a3.gradio.live\n",
            "\n",
            "This share link is temporary and will last for up to 1 week (best effort). For free permanent hosting and GPU upgrades, run `gradio deploy` from the terminal in the working directory to deploy to Hugging Face Spaces (https://huggingface.co/spaces)\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ],
            "text/html": [
              "<div><iframe src=\"https://b160c7131b34fd04a3.gradio.live\" width=\"100%\" height=\"500\" allow=\"autoplay; camera; microphone; clipboard-read; clipboard-write;\" frameborder=\"0\" allowfullscreen></iframe></div>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "hello P69905\n"
          ]
        }
      ],
      "source": [
        "import re\n",
        "import requests\n",
        "import matplotlib\n",
        "matplotlib.use(\"Agg\")          # no GUI backend in a notebook/server\n",
        "import matplotlib.pyplot as plt\n",
        "import gradio as gr\n",
        "!pip install biopython\n",
        "from Bio.SeqUtils.ProtParam import ProteinAnalysis\n",
        "\n",
        "STANDARD_AA = \"ACDEFGHIKLMNPQRSTVWY\"\n",
        "\n",
        "\n",
        "\n",
        "def fetch_sequence(uniprot_id):\n",
        "    print(\"hello\", uniprot_id)\n",
        "    url = f\"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta\"\n",
        "    r = requests.get(url, timeout=20)\n",
        "    r.raise_for_status()\n",
        "    return \"\".join(r.text.split(\"\\n\")[1:])\n",
        "'''\n",
        "\n",
        "  def fetch_uniprot_data(uniprot_id):\n",
        "    uniprot_id = uniprot_id.strip().upper()\n",
        "\n",
        "    url = f\"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json\"\n",
        "\n",
        "    r = requests.get(url, timeout=20)\n",
        "    r.raise_for_status()\n",
        "\n",
        "    data = r.json()\n",
        "\n",
        "    sequence = data[\"sequence\"][\"value\"]\n",
        "    organism = data[\"organism\"][\"scientificName\"]\n",
        "\n",
        "    protein_description = data.get(\"proteinDescription\", {})\n",
        "\n",
        "    try:\n",
        "        protein_name = (\n",
        "            protein_description[\"recommendedName\"]\n",
        "            [\"fullName\"]\n",
        "            [\"value\"]\n",
        "        )\n",
        "    except KeyError:\n",
        "        protein_name = \"Protein name not available\"\n",
        "\n",
        "    pdb_records = []\n",
        "\n",
        "    for ref in data.get(\"uniProtKBCrossReferences\", []):\n",
        "\n",
        "        if ref.get(\"database\") == \"PDB\":\n",
        "\n",
        "            properties = {}\n",
        "\n",
        "            for prop in ref.get(\"properties\", []):\n",
        "                properties[prop[\"key\"]] = prop[\"value\"]\n",
        "\n",
        "            pdb_records.append({\n",
        "                \"pdb_id\": ref[\"id\"],\n",
        "                \"method\": properties.get(\"Method\"),\n",
        "                \"resolution\": properties.get(\"Resolution\"),\n",
        "                \"chains\": properties.get(\"Chains\")\n",
        "            })\n",
        "\n",
        "    return {\n",
        "        \"uniprot_id\": uniprot_id,\n",
        "        \"protein_name\": protein_name,\n",
        "        \"organism\": organism,\n",
        "        \"sequence\": sequence,\n",
        "        \"pdb_records\": pdb_records\n",
        "    }\n",
        "\n",
        "'''\n",
        "\n",
        "def calculate_properties(sequence):\n",
        "    protein = ProteinAnalysis(sequence)\n",
        "    return {\n",
        "        \"length\": len(sequence),\n",
        "        \"molecular_weight\": round(protein.molecular_weight(), 2),\n",
        "        \"aromaticity\": round(protein.aromaticity(), 4),\n",
        "        \"instability_index\": round(protein.instability_index(), 2),\n",
        "        \"isoelectric_point\": round(protein.isoelectric_point(), 2),\n",
        "        \"gravy\": round(protein.gravy(), 4),\n",
        "        \"charge_at_pH7\": round(protein.charge_at_pH(7.0), 2),\n",
        "    }\n",
        "\n",
        "\n",
        "def plot_aa(sequence):\n",
        "    amino_acids = list(STANDARD_AA)\n",
        "    counts = [sequence.count(aa) for aa in amino_acids]\n",
        "    fig, ax = plt.subplots(figsize=(10, 4))\n",
        "    ax.bar(amino_acids, counts)\n",
        "    ax.set_xlabel(\"Amino Acid\")\n",
        "    ax.set_ylabel(\"Count\")\n",
        "    ax.set_title(\"Amino Acid Composition\")\n",
        "    fig.tight_layout()\n",
        "    return fig\n",
        "\n",
        "\n",
        "def plot_charge_vs_pH(sequence):\n",
        "    protein = ProteinAnalysis(sequence)\n",
        "    hold_charges = [protein.charge_at_pH(pH) for pH in range(2, 13)]\n",
        "    pH_values = list(range(2, 13))\n",
        "    fig, ax = plt.subplots(figsize=(10, 4))\n",
        "    ax.plot(pH_values, hold_charges, marker=\"o\", color=\"blue\")\n",
        "    ax.set_xlabel(\"pH\")\n",
        "    ax.set_ylabel(\"Predicted Net Charge\")\n",
        "    ax.set_title(\"Predicted Protein Charge vs pH\")\n",
        "    fig.tight_layout()\n",
        "    return fig\n",
        "\n",
        "\n",
        "def main_protein(uniprot_id):\n",
        "    try:\n",
        "        seq = fetch_sequence(uniprot_id.strip().upper())\n",
        "    except Exception as e:\n",
        "        return f\"Could not fetch {uniprot_id}: {e}\", None\n",
        "\n",
        "    seq = re.sub(f\"[^{STANDARD_AA}]\", \"\", seq.upper())\n",
        "    if not seq:\n",
        "        return f\"No standard residues found for {uniprot_id}\", None\n",
        "\n",
        "    props = calculate_properties(seq)\n",
        "    lines = \"\\n\".join(f\"{k}: {v}\" for k, v in props.items())\n",
        "    return f\"UniProt ID: {uniprot_id}\\n{lines}\", plot_aa(seq), plot_charge_vs_pH(seq)\n",
        "\n",
        "with gr.Blocks() as app:\n",
        "    gr.Markdown(\n",
        "        \"\"\"\n",
        "        # Protein Structure Finder\n",
        "\n",
        "        Enter a UniProt ID.\n",
        "\n",
        "        1. Search the given UniProt ID\n",
        "        2. Find associated PDB entries\n",
        "        3. Display protein properties and structures\n",
        "\n",
        "        -Arhaan\n",
        "        \"\"\"\n",
        "    )\n",
        "    uniprot_input = gr.Textbox(value=\"P69905\", label=\"UniProt ID\")\n",
        "    analyze_button = gr.Button(\"Analyze\")\n",
        "    output = gr.Textbox(label=\"Results\")\n",
        "    aa_plot_output = gr.Plot(label=\"Amino Acid Composition\")\n",
        "    plot_charge_vs_pH_output = gr.Plot(label=\"Predicted Protein Charge vs pH\")\n",
        "\n",
        "    analyze_button.click(\n",
        "        fn=main_protein,\n",
        "        inputs=uniprot_input,\n",
        "        outputs=[output, aa_plot_output, plot_charge_vs_pH_output],\n",
        "    )\n",
        "\n",
        "app.launch(share=True, debug=True)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "nk-fygQ7MxCk",
        "outputId": "8ecdd603-c892-48e9-943d-52ceb141cff9"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "hello P68871\n"
          ]
        },
        {
          "data": {
            "text/plain": [
              "('UniProt ID: P68871\\nlength: 147\\nmolecular_weight: 15998.21\\naromaticity: 0.0884\\ninstability_index: 6.16\\nisoelectric_point: 6.74\\ngravy: 0.0136\\ncharge_at_pH7: -0.72',\n",
              " <Figure size 1000x400 with 1 Axes>)"
            ]
          },
          "execution_count": 7,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "main_protein(\"P68871\")"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}