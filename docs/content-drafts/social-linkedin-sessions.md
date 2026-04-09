# LinkedIn: What 337 AI Sessions Taught Me

**Target:** LinkedIn
**Length:** ~300 words
**Tone:** Reflective, data-informed

---

I looked at 337 of my AI coding sessions for the first time.

Not one at a time -- that would take weeks. I built a tool (llm-wiki) that converts session transcripts from Claude Code, Copilot, Cursor, and other AI assistants into a searchable knowledge base. Then I actually read the patterns.

Here is what surprised me:

1. I ask the same architectural question in different ways across projects. The AI gives different answers depending on context. Without a unified view, I never noticed the contradictions.

2. My tool usage shifted dramatically over time. Early sessions were almost entirely Bash and Read commands. Six months later, I had shifted to Edit and Grep. The tool-calling bar charts made this visible at a glance.

3. The sessions I dismissed as "throwaway debugging" contained the most reusable knowledge. A 15-minute session debugging a WebSocket reconnection bug had more transferable patterns than a 2-hour architecture discussion.

4. I use different AI assistants for different strengths, but I had never made that explicit. Claude Code for complex refactoring. Copilot for quick fixes. Cursor for prototyping. Seeing the agent badges across projects made my own workflow legible to me for the first time.

5. Token usage varies wildly. Some 10-minute sessions burned more tokens than 2-hour sessions because of repeated large file reads. Knowing this changed how I structure my prompts.

None of these insights were available when the transcripts were scattered across five different tools in raw JSONL format. It took aggregating them into one searchable, visualized knowledge base.

If you use AI coding assistants daily, your session history is one of your most underutilized assets. You just need a way to read it.

llm-wiki is free, local, and open source: https://github.com/Pratiyush/llm-wiki
Live demo: https://pratiyush.github.io/llm-wiki/

#AI #DeveloperTools #LLM #Productivity #SoftwareEngineering #OpenSource
