# W1-T3 模型参数对比实验

- 问题：孩子写作业总是拖延，我应该怎么引导？
- 模型：`gpt-5-mini`

## 对比表

| 场景 | 参数 | 预期影响 | Parenting Copilot 判断 | 调用状态 | 输出摘录 |
| --- | --- | --- | --- | --- | --- |
| `stable_default` | `{"model": "gpt-5-mini", "max_output_tokens": 800}` | 不显式发送采样参数，优先观察模型默认行为。 | 适合作为教育建议的基线输出。 | payload-only | 未调用 API；本行用于观察请求参数形态。 |
| `short_budget` | `{"model": "gpt-5-mini", "max_output_tokens": 180}` | 输出预算很小，建议更容易变短或被截断。 | 不适合复杂亲子问题，容易丢失边界和步骤。 | payload-only | 未调用 API；本行用于观察请求参数形态。 |
| `long_budget` | `{"model": "gpt-5-mini", "max_output_tokens": 1400}` | 输出空间更充足，可以包含原因、步骤和注意事项。 | 适合需要解释和行动计划的问题，但要避免啰嗦。 | payload-only | 未调用 API；本行用于观察请求参数形态。 |
| `higher_temperature` | `{"model": "gpt-5-mini", "temperature": 0.9, "max_output_tokens": 800}` | 随机性更强，措辞和建议角度可能更发散。 | 可用于头脑风暴，不适合默认教育建议。 | payload-only | 未调用 API；本行用于观察请求参数形态。 |
| `lower_top_p` | `{"model": "gpt-5-mini", "top_p": 0.5, "max_output_tokens": 800}` | 候选词范围更窄，输出通常更保守。 | 可能更稳定，但也可能降低多样性和细腻度。 | payload-only | 未调用 API；本行用于观察请求参数形态。 |
| `streaming_shape` | `{"model": "gpt-5-mini", "max_output_tokens": 800, "stream": true}` | 返回方式变成流式，用户能更快看到首段内容。 | 改善等待体验，但不等于内容更可靠。 | payload-only | 未调用 API；本行用于观察请求参数形态。 |

## 初步结论

- 教育类建议默认应该更稳定：低随机性、足够输出预算、明确安全边界。
- `max_output_tokens` 太小会直接影响完整性，可能让建议缺少原因、步骤或风险提醒。
- `temperature` 或 `top_p` 更适合探索不同表达和方案，不适合作为高风险场景的默认配置。
- `streaming` 主要改善交互体验，不负责提升答案质量；内容可靠性仍要靠 prompt、结构化输出、校验和安全策略。

## 复盘问题

- 什么时候应该让模型更发散，什么时候应该更稳定？
- 如果一个回答被截断，产品上应该如何提示或自动恢复？
