/**
 * llm-wiki Obsidian plugin — minimal scaffold.
 *
 * Syncs the wiki/ folder from an llm-wiki project into the current vault,
 * preserving [[wikilinks]] which are already native Obsidian syntax.
 *
 * Build with esbuild (see Obsidian sample plugin for full setup):
 *   npx esbuild main.ts --bundle --external:obsidian --outfile=main.js --format=cjs
 */

import {
  App,
  Plugin,
  PluginSettingTab,
  Setting,
  Notice,
  TFile,
} from "obsidian";
import { exec } from "child_process";

// ---------------------------------------------------------------------------
// Settings
// ---------------------------------------------------------------------------

interface LlmwikiSettings {
  /** Absolute path to the llm-wiki project root (contains wiki/). */
  projectRoot: string;
  /** Python executable. */
  pythonPath: string;
  /** Target folder inside the vault where wiki pages are copied. */
  vaultFolder: string;
}

const DEFAULT_SETTINGS: LlmwikiSettings = {
  projectRoot: "",
  pythonPath: "python3",
  vaultFolder: "llm-wiki",
};

// ---------------------------------------------------------------------------
// Plugin
// ---------------------------------------------------------------------------

export default class LlmwikiPlugin extends Plugin {
  settings: LlmwikiSettings = DEFAULT_SETTINGS;

  async onload() {
    await this.loadSettings();

    // Command: Wiki Sync
    this.addCommand({
      id: "llmwiki-sync",
      name: "Wiki Sync",
      callback: () => this.syncWiki(),
    });

    // Command: Wiki Build
    this.addCommand({
      id: "llmwiki-build",
      name: "Wiki Build",
      callback: () => this.buildSite(),
    });

    // Settings tab
    this.addSettingTab(new LlmwikiSettingTab(this.app, this));
  }

  async onunload() {
    // Nothing to tear down.
  }

  async loadSettings() {
    this.settings = Object.assign(
      {},
      DEFAULT_SETTINGS,
      await this.loadData()
    );
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  /**
   * Run `python3 -m llmwiki sync` then copy wiki/ into the vault.
   */
  async syncWiki() {
    const { projectRoot, pythonPath, vaultFolder } = this.settings;
    if (!projectRoot) {
      new Notice("llm-wiki: Set the project root in settings first.");
      return;
    }

    new Notice("llm-wiki: syncing sessions...");

    // Step 1: run sync in the project directory
    await this.runCommand(pythonPath, ["-m", "llmwiki", "sync"], projectRoot);

    // Step 2: copy wiki/ files into the vault
    await this.copyWikiToVault(projectRoot, vaultFolder);

    new Notice("llm-wiki: sync complete.");
  }

  /**
   * Run `python3 -m llmwiki build` in the project directory.
   */
  async buildSite() {
    const { projectRoot, pythonPath } = this.settings;
    if (!projectRoot) {
      new Notice("llm-wiki: Set the project root in settings first.");
      return;
    }
    new Notice("llm-wiki: building site...");
    await this.runCommand(pythonPath, ["-m", "llmwiki", "build"], projectRoot);
    new Notice("llm-wiki: build complete.");
  }

  // -----------------------------------------------------------------------
  // Helpers
  // -----------------------------------------------------------------------

  private runCommand(
    cmd: string,
    args: string[],
    cwd: string
  ): Promise<string> {
    return new Promise((resolve, reject) => {
      exec(`${cmd} ${args.join(" ")}`, { cwd }, (err, stdout, stderr) => {
        if (err) {
          new Notice(`llm-wiki error: ${stderr || err.message}`);
          reject(err);
        } else {
          resolve(stdout);
        }
      });
    });
  }

  /**
   * Walk the wiki/ directory in the project root and mirror every .md file
   * into <vault>/<vaultFolder>/.
   *
   * This is a simplified implementation. A production version would use
   * Node's fs module with recursive directory walking.
   */
  private async copyWikiToVault(
    projectRoot: string,
    vaultFolder: string
  ): Promise<void> {
    // Obsidian's vault adapter can create files.
    // For the scaffold, we demonstrate the pattern with a placeholder.
    // A full implementation would:
    //   1. Walk projectRoot/wiki/ recursively
    //   2. For each .md file, read its contents
    //   3. Use this.app.vault.adapter.write() to place it in vaultFolder/

    const adapter = this.app.vault.adapter;
    const wikiIndexPath = `${projectRoot}/wiki/index.md`;

    // Ensure target folder exists
    if (!(await adapter.exists(vaultFolder))) {
      await adapter.mkdir(vaultFolder);
    }

    // TODO: Replace with full recursive copy.
    // For now, copy just index.md as a proof of concept.
    try {
      const fs = require("fs");
      const content = fs.readFileSync(wikiIndexPath, "utf-8");
      await adapter.write(`${vaultFolder}/index.md`, content);
    } catch (e) {
      new Notice(`llm-wiki: failed to copy index.md — ${e}`);
    }
  }
}

// ---------------------------------------------------------------------------
// Settings Tab
// ---------------------------------------------------------------------------

class LlmwikiSettingTab extends PluginSettingTab {
  plugin: LlmwikiPlugin;

  constructor(app: App, plugin: LlmwikiPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "llm-wiki Settings" });

    new Setting(containerEl)
      .setName("Project root")
      .setDesc("Absolute path to the llm-wiki repository root")
      .addText((text) =>
        text
          .setPlaceholder("/path/to/llm-wiki")
          .setValue(this.plugin.settings.projectRoot)
          .onChange(async (value) => {
            this.plugin.settings.projectRoot = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Python path")
      .setDesc("Python interpreter used to run llmwiki CLI")
      .addText((text) =>
        text
          .setValue(this.plugin.settings.pythonPath)
          .onChange(async (value) => {
            this.plugin.settings.pythonPath = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Vault folder")
      .setDesc("Folder inside the vault where wiki pages are synced")
      .addText((text) =>
        text
          .setValue(this.plugin.settings.vaultFolder)
          .onChange(async (value) => {
            this.plugin.settings.vaultFolder = value;
            await this.plugin.saveSettings();
          })
      );
  }
}
