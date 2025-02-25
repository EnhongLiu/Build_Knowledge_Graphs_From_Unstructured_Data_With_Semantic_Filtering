from databricks_langchain import ChatDatabricks
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
import numpy as np
import pandas as pd
import json


def graphPrompt(input_text: str, metadata:{}):

    SYS_PROMPT = """
        You are a network graph maker specializing in dairy science, extracting terms and their relations from a given context. You are provided with a context chunk (delimited by ```) from the Journal of Dairy Science® (JDS). Your task is to extract the ontology of terms mentioned in the given context, focusing on key concepts in dairy science.

        Step 1: While traversing through each sentence, identify the key terms mentioned in it. Terms may include dairy-related objects, entities, processes, technologies, or concepts such as:
            - Dairy products: milk, cheese, yogurt, butter, etc.
            - Animals: dairy cows, calves, heifers, cattle breeds (e.g., Holstein, Jersey), etc.
            - Nutrition: feed, forage, silage, total mixed ration (TMR), concentrates, supplements (e.g., vitamins, minerals), etc.
            - Health: mastitis, lameness, metabolic disorders (e.g., ketosis, milk fever), vaccines, antibiotics, etc.
            - Genetics: breeding, genomics, heritability, genetic markers, selective breeding, etc.
            - Reproduction: artificial insemination, embryo transfer, estrus synchronization, fertility, etc.
            - Management: milking systems (e.g., robotic milking), herd management, housing systems, sustainability practices, etc.
            - Environment: greenhouse gas emissions, manure management, water usage, etc.
            - Processing and technology: pasteurization, homogenization, fermentation, ultrafiltration, packaging, etc.
            - Scientific domains: biochemistry, microbiology, genetics, nutrition, pathology, physiology, etc.
            - Organizations and entities: American Dairy Science Association®, government agencies, research institutions, etc.
            - Conditions and factors: milk composition (e.g., fat, protein), shelf life, spoilage, food safety, etc.
            - Terms should be as specific and atomistic as possible.

        Step 2: Identify how these terms are related to one another. Terms mentioned in the same sentence or paragraph are typically related. Relationships can include, but not limited to:
            - Process relationships: e.g., "pasteurization affects milk shelf life."
            - Compositional relationships: e.g., "milk contains lactose."
            - Causal relationships: e.g., "microbial contamination causes spoilage."
            - Functional relationships: e.g., "probiotics improve gut health."
            - Biological relationships: e.g., "genetic markers influence milk yield."
            - Management relationships: e.g., "feeding practices impact milk composition."
            - Environmental relationships: e.g., "manure management affects greenhouse gas emissions."

        Step 3: Define the relationship between each pair of related terms. Format your output ONLY as a JSON list but NOTHING ELSE:
            [
                {
                    "node_1": "A concept from extracted ontology",
                    "node_2": "A related concept from extracted ontology",
                    "edge": "Relationship between the two concepts, node_1 and node_2 in one or two sentences"
                },
                ...
            ]

    ----Example----

    Context: "Feeding cows a high-forage diet improves milk fat content, while genetic selection can enhance milk yield and disease resistance. Additionally, robotic milking systems reduce labor costs and improve milking efficiency."

    Output:
            [
        {
            "node_1": "high-forage diet",
            "node_2": "milk fat content",
            "edge": "Feeding cows a high-forage diet improves milk fat content."
        },
        {
            "node_1": "genetic selection",
            "node_2": "milk yield",
            "edge": "Genetic selection can enhance milk yield in dairy cows."
        },
        {
            "node_1": "genetic selection",
            "node_2": "disease resistance",
            "edge": "Genetic selection can improve disease resistance in dairy cows."
        },
        {
            "node_1": "robotic milking systems",
            "node_2": "labor costs",
            "edge": "Robotic milking systems reduce labor costs in dairy farming."
        },
        {
            "node_1": "robotic milking systems",
            "node_2": "milking efficiency",
            "edge": "Robotic milking systems improve milking efficiency."
        }
    ]

    Note: Focus on extracting relationships that are explicitly stated or strongly implied in the context. Avoid speculative or inferred relationships unless they are well-supported by the text.

    """

    messages = [
        {"role": "system", "content": SYS_PROMPT},
        {"role": "user", "content": f"context: ```{input_text}```"}
    ]

    llama70b = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.0,
    max_tokens=1024,
    streaming=True
    )

    response = llama70b.invoke(messages)
    response_content = response.content
    
    try:
        result = json.loads(response_content)
        result = [dict(item, **metadata) for item in result]
    except json.JSONDecodeError:
        print("\n\nERROR ### Here is the buggy response: ", response_content, "\n\n")
        result = None
    
    return result


def df2Graph(dataframe: pd.DataFrame) -> list:
    # dataframe.reset_index(inplace=True)
    results = dataframe.apply(
        lambda row: graphPrompt(row.text, {"chunk_id": row.chunk_id}), axis=1
    )
    # invalid json results in NaN
    results = results.dropna()
    results = results.reset_index(drop=True)

    ## Flatten the list of lists to one single list of entities.
    concept_list = np.concatenate(results).ravel().tolist()
    return concept_list


def graph2Df(nodes_list) -> pd.DataFrame:
    ## Remove all NaN entities
    graph_dataframe = pd.DataFrame(nodes_list).replace(" ", np.nan)
    graph_dataframe = graph_dataframe.dropna(subset=["node_1", "node_2"])
    graph_dataframe["node_1"] = graph_dataframe["node_1"].apply(lambda x: x.lower())
    graph_dataframe["node_2"] = graph_dataframe["node_2"].apply(lambda x: x.lower())

    return graph_dataframe


regenerate = True #Set as True to regenerate the data, otherwise, just read in the csv
df_to_be_graphed = df_chunks
if regenerate:
    concepts_list = df2Graph(df_to_be_graphed)
    dfg1 = graph2Df(concepts_list)
 else:
    dfg1 = pd.read_csv("./graph.csv", sep="|")
