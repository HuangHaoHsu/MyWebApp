# 环境变量使用说明

## 本地开发环境配置

1. 将 `.env.example` 文件复制并重命名为 `.env`（注意前面有个点）
2. 在 `.env` 文件中填入你的API密钥信息
3. 这个文件会被 .gitignore 忽略，不会被提交到Git仓库，保证安全

## Vercel部署环境配置

当部署到Vercel时，请在Vercel项目设置中添加环境变量：

1. 登录Vercel账户
2. 进入你的项目
3. 点击 "Settings" -> "Environment Variables"
4. 添加与 `.env` 文件中相同的环境变量和值

## 环境变量说明

使用以下任一组API密钥即可（按优先级排序）：

### Azure OpenAI API（推荐）
- `AZURE_OPENAI_API_KEY`: Azure OpenAI的API密钥
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI的端点URL，例如 "https://your-resource.openai.azure.com"
- `AZURE_OPENAI_DEPLOYMENT_NAME`: 部署的模型名称，例如 "gpt-35-turbo"、"gpt-4"、"gpt-4-turbo"、"gpt-4-vision"、"text-embedding-ada-002" 等

### OpenAI API
- `OPENAI_API_KEY`: OpenAI的API密钥
- `OPENAI_MODEL`: 可选，模型名称，例如 "gpt-3.5-turbo"、"gpt-4"、"gpt-4-turbo"、"gpt-4-vision-preview" 等，默认为 "gpt-3.5-turbo"

### HuggingFace API
- `HUGGINGFACE_API_KEY`: HuggingFace的API Token
- `HUGGINGFACE_MODEL`: 可选，模型ID，例如 "THUDM/chatglm3-6b"、"meta-llama/Llama-2-7b-chat-hf"、"mistralai/Mistral-7B-Instruct-v0.2" 等，默认为 "THUDM/chatglm3-6b"

注意：如果没有配置任何API密钥，应用会使用内置的备用诗句，仍然能正常运行。
