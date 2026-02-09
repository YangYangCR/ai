#transformers 是 hugging face开源库
from transformers import AutoTokenizer, AutoModelForCausalLM, GPT2Tokenizer, GPT2LMHeadModel


def gpt_demo():
    model_name = "IDEA-CCNL/Wenzhong-GPT2-110M"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="float32"
    )

    prompt = "今天的天气"
    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        return_dict_in_generate=True,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.8,
        max_length=100,
        num_return_sequences=5
    )

    for idx, sentence in enumerate(outputs.sequences):
        print(tokenizer.decode(sentence))

    # print(tokenizer.decode(outputs[0], skip_special_tokens=True))


def hug_demo():
    hf_model_path = 'IDEA-CCNL/Wenzhong-GPT2-110M'
    tokenizer = GPT2Tokenizer.from_pretrained(hf_model_path)
    model = GPT2LMHeadModel.from_pretrained(hf_model_path)
    question = "北京是中国的"
    inputs = tokenizer(question, return_tensors='pt')
    generation_output = model.generate(**inputs,
                                       return_dict_in_generate=True,
                                       output_scores=True,
                                       max_length=150,
                                       # max_new_tokens=80,
                                       do_sample=True,
                                       top_p=0.6,
                                       # num_beams=5,
                                       eos_token_id=50256,
                                       pad_token_id=0,
                                       num_return_sequences=5)

    for idx, sentence in enumerate(generation_output.sequences):
        print('next sentence %d:\n' % idx,
              tokenizer.decode(sentence).split('<|endoftext|>')[0])
        print('*' * 40)


if __name__ == "__main__":
    gpt_demo()
