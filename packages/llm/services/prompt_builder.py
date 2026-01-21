"""Prompt builder for LLM system instructions."""
from typing import Dict, Optional


class PromptBuilder:
    """Build system instructions for LLMs."""

    def __init__(self, product_name: str = "AI Assistant", company_name: str = "Company"):
        self.product_name = product_name
        self.company_name = company_name

    def build_system_instruction(
        self,
        role: str = "assistant",
        language: str = "pt-BR",
        focus: Optional[str] = None,
        tone: str = "professional",
    ) -> str:
        """Build system instruction."""
        base = f"Você é {self.product_name}, criado pela {self.company_name}.\n\n"

        roles = {
            "assistant": "Responda de forma clara e direta.",
            "tutor": "Explique conceitos de forma didática com analogias.",
            "senior": "Forneça análises técnicas profundas e melhores práticas.",
            "debug": "Analise problemas tecnicamente e forneça soluções práticas.",
        }

        base += roles.get(role, roles["assistant"]) + "\n\n"

        if focus:
            base += f"Foco: {focus}\n\n"

        tones = {
            "professional": "Tom profissional e objetivo.",
            "friendly": "Tom amigável e conversacional.",
            "technical": "Tom técnico e preciso.",
        }

        base += tones.get(tone, tones["professional"]) + "\n\n"

        languages = {
            "pt-BR": "Responda em Português do Brasil.",
            "en-US": "Answer in English.",
            "es-ES": "Responde en Español.",
        }

        base += languages.get(language, languages["pt-BR"])

        return base

    def build_pedagogical_prompt(self, subject: str = "Geral") -> str:
        """Build pedagogical system instruction."""
        return f"""Você é {self.product_name}, um mentor de tecnologia sênior.

Sua missão é explicar conceitos de forma simples e didática.

Estrutura de resposta:
1. Explicação direta e simples
2. Analogia do mundo real
3. Curiosidade ou fato histórico
4. Referências para aprofundar

Tom: Empático, motivador e levemente bem-humorado.
Contexto: O aluno está estudando {subject}.
Idioma: Português do Brasil."""
