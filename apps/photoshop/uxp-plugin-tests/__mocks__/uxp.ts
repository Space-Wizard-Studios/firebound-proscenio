// Vitest host mock for the UXP "uxp" module, wired in through
// vitest.config.ts test.alias. Minimal surface for the storage / xmp
// imports in the file-IO api modules; extend as those gain unit tests.

import { vi } from "vitest";

export const storage = {
    localFileSystem: {
        getFolder: vi.fn(),
        getFileForOpening: vi.fn(),
        createSessionToken: vi.fn(),
    },
    formats: { utf8: "utf8" },
};

export const xmp: Record<string, unknown> = {};
