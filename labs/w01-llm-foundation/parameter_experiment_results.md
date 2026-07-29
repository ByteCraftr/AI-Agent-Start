# W1-T3 模型参数对比实验

- 问题：孩子写作业总是拖延，我应该怎么引导？
- 模型：`gpt-5-mini`

## 对比表

| 场景 | 参数 | 预期影响 | Parenting Copilot 判断 | 调用状态 | 输出摘录 |
| --- | --- | --- | --- | --- | --- |
| `stable_default` | `{"model": "gpt-5-mini", "max_output_tokens": 800}` | 不显式发送采样参数，优先观察模型默认行为。 | 适合作为教育建议的基线输出。 | ok | 孩子写作业拖延是常见问题，通常不是孩子不听话，而是跟习惯、注意力、任务感到吃力、时间管理能力或环境有关。下面给你一套实用、低风险的引导方法与具体话术，方便马上试用并根据效果调整。<br><br>一、先做短暂观察（1周）<br>- 记录什么时候最拖、拖多久、拖的是什么类型作业（写字、算题、读书、上网提交等）。<br>- 观察外部因素：是否饿、困、情绪不好、手机在旁、作业量太大或难度超出能力。<br><br>二、搭建稳定流程（routine）<br>- 固定“放学→休息/加餐→写作业”的顺序。稳定仪式能减少磨蹭。例如：回家后先吃点水果、休息20分钟，再开始作业。<br>- 给出明确开始时间和预计时长：比如“下午5:00开始，先做30分钟，然后休息10分钟”。<br><br>三、把任务拆小块（chunking）+ 用... |
| `short_budget` | `{"model": "gpt-5-mini", "max_output_tokens": 180}` | 输出预算很小，建议更容易变短或被截断。 | 不适合复杂亲子问题，容易丢失边界和步骤。 | error | API 调用成功，但没有提取到文本输出。 |
| `long_budget` | `{"model": "gpt-5-mini", "max_output_tokens": 1400}` | 输出空间更充足，可以包含原因、步骤和注意事项。 | 适合需要解释和行动计划的问题，但要避免啰嗦。 | ok | 孩子写作业老拖延是很常见的事，家长可以用结构、情感支持和技能训练三方面去引导。下面给你一套可操作的步骤、话术和注意事项，方便立刻试用并逐步调整。<br><br>核心原则（先记住）<br>- 以建立规律为主，避免一次性改变太多。<br>- 给孩子选择与自主权，减少对抗感。<br>- 强化过程（付出和开始），而非只看结果。<br>- 观察是否有学习困难、注意力、情绪问题，必要时向老师或专业人员咨询。<br><br>具体策略（可按年龄和情况调整）<br>1. 观察并记录<br>- 先一周观察：什么时间、哪类作业、什么情境下拖延最多。找出模式（比如数学题、晚饭后疲惫、手机干扰）。<br><br>2. 制定固定作业时间和环境<br>- 固定“作业开始窗”而非严格时刻，例如“晚饭后休息20分钟——7:00到8:00是做作业... |
| `higher_temperature` | `{"model": "gpt-5-mini", "temperature": 0.9, "max_output_tokens": 800}` | 随机性更强，措辞和建议角度可能更发散。 | 可用于头脑风暴，不适合默认教育建议。 | error | OpenAI API returned HTTP 400: {
  "error": {
    "message": "Unsupported parameter: 'temperature' is not supported with this model.",
    "type": "invalid_request_error",
    "param": "temperature",
    "code": null
  }
} |
| `lower_top_p` | `{"model": "gpt-5-mini", "top_p": 0.5, "max_output_tokens": 800}` | 候选词范围更窄，输出通常更保守。 | 可能更稳定，但也可能降低多样性和细腻度。 | error | OpenAI API returned HTTP 400: {
  "error": {
    "message": "Unsupported parameter: 'top_p' is not supported with this model.",
    "type": "invalid_request_error",
    "param": "top_p",
    "code": null
  }
} |
| `streaming_shape` | `{"model": "gpt-5-mini", "max_output_tokens": 800, "stream": true}` | 返回方式变成流式，用户能更快看到首段内容。 | 改善等待体验，但不等于内容更可靠。 | skipped | streaming 场景本脚本只记录请求形态，不做 SSE 解析。 |

## 初步结论

- 教育类建议默认应该更稳定：低随机性、足够输出预算、明确安全边界。
- `max_output_tokens` 太小会直接影响完整性，可能让建议缺少原因、步骤或风险提醒。
- `temperature` 或 `top_p` 更适合探索不同表达和方案，不适合作为高风险场景的默认配置。
- `streaming` 主要改善交互体验，不负责提升答案质量；内容可靠性仍要靠 prompt、结构化输出、校验和安全策略。

## 复盘问题

- 什么时候应该让模型更发散，什么时候应该更稳定？
- 如果一个回答被截断，产品上应该如何提示或自动恢复？
