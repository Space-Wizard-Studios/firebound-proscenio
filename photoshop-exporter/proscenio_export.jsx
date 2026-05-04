// Proscenio — Photoshop exporter
// Exports visible layers as PNG plus a position JSON suitable for the
// Proscenio Blender addon.
//
// Compatible with Photoshop CC 2015 and later.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#target photoshop

(function () {
    if (!app.documents.length) {
        alert("Open a document first.");
        return;
    }

    // Scaffold — implementation lands during Phase 1.
    // See .ai/skills/photoshop-jsx-dev.md for output schema and conventions.
    alert("Proscenio JSX exporter — scaffold. Implementation pending.");
})();
