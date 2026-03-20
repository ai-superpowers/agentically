# Glossary

Terms and definitions used throughout the agentically documentation.

| Term                | Definition                                                                                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent system        | A named collection of AI prompt, skill, and memory files distributed through the agentically registry and installed with `agentically create`.                       |
| Memory              | A directory within an agent system that holds configuration and in-progress state files; routed to `<platform_dir>/memory/` on the user's machine upon installation. |
| Platform adaptation | The process of routing an installed agent system's files into a coding platform's specific directory layout using a `PlatformAdapter`.                               |
| PlatformAdapter     | Base class that maps an agent-relative file path to its final installed location on disk for a given coding platform.                                                |
| Prompt              | A markdown instruction file for an AI coding assistant, installed into the platform's designated prompts subdirectory.                                               |
| Registry            | The GitHub repository (`ai-superpowers/agentically`) hosting community-maintained agent systems under `prompt-systems/`, browsed via `agentically explore`.          |
| Skill               | A specialized markdown instruction file providing domain-specific AI guidance, installed into the platform's skills subdirectory.                                    |
