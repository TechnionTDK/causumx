import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

def causumx_output_to_natural_language_explanation(causumx_output):
    insights = []

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

        def format_number(n):
            """Format the number as 10K instead of 10000."""
            if abs(n) >= 1000:
                return f"{n / 1000:.1f}K"
            return str(n)

        insights.append(
            f"{i + 1}️⃣ For the group defined by {group_key}: '{group_value}', the most substantial positive effect on {target_class} (effect size of {format_number(cate_h)}) is observed for {t_h_key}: {t_h_value}, while the most substantial negative effect (effect size of {format_number(cate_l)}) is observed for {t_l_key}: {t_l_value}.\n")


    return insights

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