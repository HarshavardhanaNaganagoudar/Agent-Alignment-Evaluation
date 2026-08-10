# Agent Alignment Evaluation

> Can an autonomous AI agent remain honest, safe, and corrigible when
> deception and rule-breaking increase its reward?

An autonomous AI agent that manages a water bottle vending machine using a local LLM (gemma4:12b) via Ollama. The agent makes business decisions, responds to customer events, adjusts pricing, manages inventory, and aims to maximize long-term profit.

This project evaluates autonomous AI agents in simulated business
environments designed to create conflicts between an agent's objective
and desirable behavioral constraints.

The agent is given a simple objective:

> Maximize final account balance.

It is then exposed to situations where achieving that objective may
incentivize:

- Deception
- Concealing errors
- Scapegoating humans
- Ignoring safety warnings
- Exploiting information asymmetry
- Anti-competitive coordination
- Risk-taking for financial gain

The goal is not to prove that a model is "aligned" or "misaligned"
from a single run.

Instead, this project documents observable behaviors and asks:

> What does an autonomous agent do when undesirable behavior becomes
> instrumentally useful for achieving its objective?

# Deceptive behaviour findings and evidence

**[Findings](./findings)**
