# Prompt autocomplete for Antigravity

This Windows helper turns the natural-language examples in
`workflows/natural-language-triggers.md` into suggestions inside Antigravity's
Agent input. It has no absolute repository path and needs no third-party package.

## Start

From the cloned `.agent` repository:

```bat
prompt-autocomplete.bat
```

The batch launcher resolves the repository from its own location and starts the
helper in a minimized Windows PowerShell window. The direct PowerShell command is
also available:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\prompt-autocomplete\Start-PromptAutocomplete.ps1
```

Keep that PowerShell process open. In an Antigravity Agent input, type a prefix
such as `Làm tính năng `. Matching complete prompts appear below the input.

- `Up` / `Down`: select a suggestion.
- `Tab` or `Enter`: insert it.
- `Esc`: close the list.

The helper only activates when the foreground process name or window title
contains `Antigravity`. Override that filter when needed:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\prompt-autocomplete\Start-PromptAutocomplete.ps1 -WindowTitlePattern 'Antigravity|My IDE'
```

## Updating suggestions

Edit `workflows/natural-language-triggers.md`. Restart the helper to reload the
catalog. Quoted Markdown bullets are discovered automatically, so no duplicate
JSON catalog is required.

The reader supports both native Windows text boxes (`ValuePattern`) and Chromium
or Electron content-editable inputs (`TextPattern`). The latter is the input type
used by Antigravity's Agent panel.

## Portability

All paths are derived from the launcher's own location. Cloning the repository to
another folder or machine does not require path edits. Windows PowerShell 5.1 is
built into supported Windows installations. When launched from PowerShell 7, the
launcher automatically delegates to Windows PowerShell for desktop UI support.
