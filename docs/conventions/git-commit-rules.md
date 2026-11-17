## Git Workflow Configuration

### Branch Management
- Always create a new branch for each feature or fix
- Branch names should reflect the current changes using broadly descriptive naming conventions
- Analyze the current modifications to determine appropriate branch names

### Commit Message Format

#### Structure
`[Modify] – [Brief description of the main change/integration]`

#### Prefixes
- `[Additions]` - New features, components, or functionality
- `[Modification]` - Changes to existing code or systems
- `[Fix]` - Bug fixes and corrections

#### Guidelines
- First line: Provide a detailed description of the branch name/main change
- Empty line: Always include one blank line after the first line
- Subsequent changes: Categorize all changes using the specified prefixes
- **Do not include Claude Code tags**: Never add "🤖 Generated with [Claude Code]" or "Co-Authored-By: Claude" tags to commit messages or pull request descriptions

#### Example Format
```
[Modify] – Integrate signing tool functionality and improve UART communication mechanism

[Additions] – Add SignCore implementation for RSA signing functionality
[Additions] – Add signature-related UI controls and validation in MainWindow
[Additions] – Add signing parameters support in UpgradeModelWorker
[Modification] – Update serial port management with automatic disconnection on timeout
[Modification] – Improve baudrate change handling with proper state management
[Modification] – Convert all Chinese comments to English across the codebase
[Fix] – Fix clazy warnings for range-loop detachment in Qt containers
[Fix] – Fix RSA padding bytes to match Python implementation (0x00 vs 0x01)
[Fix] – Fix serial port state management to prevent connection queue issues
```

### Instructions for Claude Code
When making commits, please:
- Analyze the current changes to determine an appropriate branch name
- Create a new branch with descriptive naming
- Format commit messages exactly as specified above
- Ensure the first line provides comprehensive context
- Categorize all changes appropriately under the three main types
- Use clear, concise descriptions for each change
- Apply the same no-Claude-tags rule to pull request descriptions

## Commit Message Guidelines

- Do not add any Claude tags to commit messages or pull request descriptions
- Commit messages should focus on describing the actual changes and their purpose
- Maintain clarity and technical precision in commit message descriptions