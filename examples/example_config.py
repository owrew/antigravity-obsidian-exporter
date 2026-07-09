"""
example_config.py
=================
Example configuration for running the Antigravity Obsidian Exporter.
Copy this file and adjust the paths to match your setup.
"""
from agy_exporter import ExporterConfig, run_export

config = ExporterConfig(
    # Path to your Antigravity workspace root.
    # This is the folder that contains brain/ and conversations/ subdirectories.
    source_dir="/path/to/antigravity/workspace",

    # Path to your Obsidian vault root.
    # Notes will be written to: {vault_dir}/AI Vault/Chats/
    vault_dir="/path/to/obsidian/vault",

    # Set to True to skip idempotency checks and rebuild every note.
    force=False,

    # Set to True to write decode-error blobs to .agy_debug/
    debug=False,

    # Set to True to exclude tool output blocks from notes (shorter notes).
    no_tool_results=False,

    # Maximum tool result blocks shown per turn (default 5, None = unlimited).
    max_tool_results_per_turn=5,

    # Filter to specific conversation IDs (list of UUID strings), or None for all.
    conv_filter=None,

    # Enable verbose logging.
    verbose=False,
)

if __name__ == "__main__":
    stats = run_export(config)
    print(f"Written: {stats['written']}  Skipped: {stats['skipped']}  Failed: {stats['failed']}")
