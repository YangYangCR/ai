import torch
import torch.nn as nn
import torch.optim as optim

# ========= 1. 准备数据 =========
text = "今天天气很好我们一起去公园玩今天天气不好我们在家学习机器学习很有趣深度学习"

# 构建字符级词表
chars = list(set(text))
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for ch, i in stoi.items()}

vocab_size = len(chars)

# 编码数据
data = torch.tensor([stoi[c] for c in text], dtype=torch.long)

# ========= 2. 定义模型 =========
class MiniGPT(nn.Module):
    def __init__(self, vocab_size, embed_size=64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.GRU(embed_size, embed_size, batch_first=True)
        self.fc = nn.Linear(embed_size, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        out, _ = self.rnn(x)
        logits = self.fc(out)
        return logits

model = MiniGPT(vocab_size)

# ========= 3. 训练 =========
optimizer = optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()

seq_len = 5

for epoch in range(200):
    total_loss = 0

    for i in range(len(data) - seq_len):
        x = data[i:i+seq_len].unsqueeze(0)
        y = data[i+1:i+seq_len+1].unsqueeze(0)

        logits = model(x)
        loss = loss_fn(logits.view(-1, vocab_size), y.view(-1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Loss: {total_loss:.4f}")

# ========= 4. 推理（生成文本） =========
def generate(start_text, length=20):
    model.eval()
    input_ids = torch.tensor([stoi[c] for c in start_text], dtype=torch.long).unsqueeze(0)

    for _ in range(length):
        logits = model(input_ids)
        next_token_logits = logits[0, -1]
        next_id = torch.argmax(next_token_logits).item()

        input_ids = torch.cat([input_ids, torch.tensor([[next_id]])], dim=1)

    return ''.join([itos[i] for i in input_ids[0].tolist()])

# 测试生成
print("\n生成结果：")
print(generate("深度"))
