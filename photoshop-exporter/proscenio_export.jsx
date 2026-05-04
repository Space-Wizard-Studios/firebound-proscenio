// Proscenio — Photoshop exporter
// Exports visible layers as PNG plus a position JSON suitable for the
// Proscenio Blender addon.
//
// Output shape (matches .ai/skills/photoshop-jsx-dev.md):
//
//   <doc>.json
//   <doc>/images/<layer>.png
//
//   {
//     "doc": "goblin.psd",
//     "size": [1024, 1024],
//     "layers": [
//       { "name": "torso", "path": "goblin/images/torso.png",
//         "position": [120, 340], "size": [180, 240] }
//     ]
//   }
//
// Conventions: hidden layers skipped, layer names prefixed `_` skipped, layer
// groups walked recursively (output names join with `__`). Compatible with
// Photoshop CC 2015 and later — uses `var`, string concatenation, no arrow
// functions or template literals.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#target photoshop

(function () {
    if (!app.documents.length) {
        alert("Open a document first.");
        return;
    }

    var doc = app.activeDocument;
    var docPath = doc.path;
    var docName = doc.name.replace(/\.[^.]+$/, "");
    var outDir = new Folder(docPath + "/" + docName);
    var imagesDir = new Folder(outDir + "/images");
    if (!outDir.exists) outDir.create();
    if (!imagesDir.exists) imagesDir.create();

    var savedRulerUnits = app.preferences.rulerUnits;
    app.preferences.rulerUnits = Units.PIXELS;

    var entries = [];
    walkLayers(doc.layers, "", entries);

    var manifest = {
        doc: doc.name,
        size: [doc.width.as("px"), doc.height.as("px")],
        layers: entries
    };

    var manifestFile = new File(outDir + "/" + docName + ".json");
    manifestFile.encoding = "UTF-8";
    manifestFile.open("w");
    manifestFile.write(stringifyManifest(manifest));
    manifestFile.close();

    app.preferences.rulerUnits = savedRulerUnits;

    alert(
        "Proscenio export complete:\n" +
        entries.length + " layer(s) → " + outDir.fsName
    );

    function walkLayers(layers, prefix, out) {
        for (var i = 0; i < layers.length; i++) {
            var layer = layers[i];
            if (!layer.visible) continue;
            if (layer.name.charAt(0) === "_") continue;

            var path = prefix === "" ? layer.name : prefix + "__" + layer.name;

            if (layer.typename === "LayerSet") {
                walkLayers(layer.layers, path, out);
                continue;
            }

            var entry = exportLayer(layer, path);
            if (entry !== null) out.push(entry);
        }
    }

    function exportLayer(layer, name) {
        var bounds = layer.bounds;
        var x = bounds[0].as("px");
        var y = bounds[1].as("px");
        var w = bounds[2].as("px") - x;
        var h = bounds[3].as("px") - y;
        if (w <= 0 || h <= 0) return null;

        // Duplicate layer into a new doc and save PNG. This trims to the
        // layer's bounds and avoids state mutations on the source document.
        var safeName = name.replace(/[^A-Za-z0-9_\-]/g, "_");
        var pngFile = new File(imagesDir + "/" + safeName + ".png");

        var workDoc = app.documents.add(
            doc.width, doc.height, doc.resolution,
            "proscenio_export_tmp", NewDocumentMode.RGB,
            DocumentFill.TRANSPARENT
        );
        app.activeDocument = doc;
        var dup = layer.duplicate(workDoc, ElementPlacement.PLACEATBEGINNING);
        app.activeDocument = workDoc;
        workDoc.trim(TrimType.TRANSPARENT);

        var pngOpts = new PNGSaveOptions();
        pngOpts.interlaced = false;
        pngOpts.compression = 9;
        workDoc.saveAs(pngFile, pngOpts, true, Extension.LOWERCASE);
        workDoc.close(SaveOptions.DONOTSAVECHANGES);
        app.activeDocument = doc;

        return {
            name: name,
            path: docName + "/images/" + safeName + ".png",
            position: [Math.round(x), Math.round(y)],
            size: [Math.round(w), Math.round(h)]
        };
    }

    function stringifyManifest(m) {
        // Photoshop CC 2015+ ships JSON.stringify; on older versions a
        // polyfill would be needed. Indent for readable diffs.
        if (typeof JSON !== "undefined" && JSON.stringify) {
            return JSON.stringify(m, null, 2);
        }
        return manualStringify(m);
    }

    function manualStringify(m) {
        var parts = [];
        parts.push('  "doc": ' + quote(m.doc) + ",");
        parts.push('  "size": [' + m.size[0] + ", " + m.size[1] + "],");
        parts.push('  "layers": [');
        for (var i = 0; i < m.layers.length; i++) {
            var L = m.layers[i];
            var trail = i === m.layers.length - 1 ? "" : ",";
            parts.push(
                '    { "name": ' + quote(L.name) +
                ', "path": ' + quote(L.path) +
                ", \"position\": [" + L.position[0] + ", " + L.position[1] + "]" +
                ", \"size\": [" + L.size[0] + ", " + L.size[1] + "] }" + trail
            );
        }
        parts.push("  ]");
        return "{\n" + parts.join("\n") + "\n}\n";
    }

    function quote(s) {
        return "\"" + String(s).replace(/\\/g, "\\\\").replace(/"/g, "\\\"") + "\"";
    }
})();
