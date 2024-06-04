import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

def causumx_output_to_natural_language_explanation(causumx_output):
    explanation = "💬 Causal Explanation\n"

    solution_details = causumx_output["solution_details"]
    for i, detail in enumerate(solution_details):
        group = detail["group"]
        group_dict = eval(group)
        group_key = list(group_dict.keys())[0]
        group_value = group_dict[group_key]

        size = detail["details"]["size"]
        covered = ", ".join(detail["details"]["covered"])
        t_h_key = list(detail["details"]["t_h"].keys())[0]
        t_h_value = detail["details"]["t_h"][t_h_key]
        cate_h = detail["details"]["cate_h"]
        t_l_key = list(detail["details"]["t_l"].keys())[0]
        t_l_value = detail["details"]["t_l"][t_l_key]
        cate_l = detail["details"]["cate_l"]
        explainability = detail["details"]["explainability"]
        target_class = causumx_output["target_class"]

        explanation += f"{i + 1}️⃣ For the group defined by {group_key}: '{group_value}', the most substantial effect on {target_class} (effect size of {cate_h:.2f}) is observed for {t_h_key}: '{t_h_value}', while the most substantial negative effect (effect size of {cate_l:.2f}) is observed for {t_l_key}: '{t_l_value}'.\n"

    # {'insight_1': 'In the United States, males have the most substantial positive effect on ConvertedSalary with an effect size of 25400.23, whereas individuals aged 18 - 24 years old have the most substantial negative effect with an effect size of -30018.80.', 'insight_2': 'In the EU, individuals aged 35 - 44 years old have the most substantial positive effect on ConvertedSalary with an effect size of 37826.78, while those aged 18 - 24 years old have the most substantial negative effect with an effect size of -46248.73.', 'insight_3': 'For regions with a medium GINI index, individuals aged 35 - 44 years old have the most substantial positive effect on ConvertedSalary with an effect size of 34809.47, while those aged 18 - 24 years old have the most substantial negative effect with an effect size of -43843.59.', 'insight_4': 'In regions with a medium GDP, individuals aged 35 - 44 years old have the most substantial positive effect on ConvertedSalary with an effect size of 31349.81, whereas those aged 18 - 24 years old have the most substantial negative effect with an effect size of -44668.45.', 'insight_5': 'For regions with a high GINI index, individuals aged 35 - 44 years old have the most substantial positive effect on ConvertedSalary with an effect size of 38620.69, while South Asians have the most substantial negative effect with an effect size of -58763.74.', 'insight_6': 'In regions with a high HDI, individuals aged 35 - 44 years old have the most substantial positive effect on ConvertedSalary with an effect size of 23179.98, whereas those aged 18 - 24 years old have the most substantial negative effect with an effect size of -41697.41.'}

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You get a list of statements. You output a JSON object: {\"insight_1\": \"<the insight as human understandable text>\", \"insight_2\": \"<the insight as human understandable text>\", ...}"
        }
      ]
    },
            {

                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Input:\n\n{explanation}"
                    }
                ]
            },
        ],
        temperature=1,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return json.loads(response.choices[0].message.content)



def main():
    causumx_output = json.load(open("causumx_json_response_example.json"))
    explanation = causumx_output_to_natural_language_explanation(causumx_output)
    print(explanation)

if __name__ == "__main__":
    main()