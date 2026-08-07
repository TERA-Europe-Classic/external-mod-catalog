#!/usr/bin/env node
/**
 * PRD 3.8.6.catalog-readme-schema.
 *
 * Compares the schema table in README.md (between the
 * `<!-- schema-table-begin -->` / `<!-- schema-table-end -->` markers)
 * against the union of keys actually used across every entry in
 * catalog.json.
 *
 * Fails when either side has a field the other doesn't — so the README
 * can't silently drift from reality, and no one can ship a new field in
 * catalog.json without documenting it for contributors.
 */

import fs from 'node:fs';
import path from 'node:path';

const REPO_ROOT = path.resolve(import.meta.dirname, '..');
const README_PATH = path.join(REPO_ROOT, 'README.md');
const CATALOG_PATH = path.join(REPO_ROOT, 'catalog.json');

const BEGIN_MARKER = '<!-- schema-table-begin -->';
const END_MARKER = '<!-- schema-table-end -->';

/**
 * Extract the set of documented field names from a markdown schema table
 * wrapped in the begin/end markers. Each data row's first pipe-cell is
 * the field name wrapped in backticks.
 *
 * Returns `{ fields, error }`. `error` is non-null when the markers are
 * missing or the table is malformed.
 */
export function extractDocumentedFields(readmeText) {
    const begin = readmeText.indexOf(BEGIN_MARKER);
    const end = readmeText.indexOf(END_MARKER);
    if (begin < 0 || end < 0 || end < begin) {
        return { fields: [], error: 'schema table markers missing or out of order' };
    }
    const block = readmeText.slice(begin + BEGIN_MARKER.length, end);
    const lines = block.split('\n');
    const fields = [];
    for (const raw of lines) {
        const line = raw.trim();
        if (!line.startsWith('|')) continue;
        // Skip header + separator rows.
        if (/^\|\s*(Field|:?-)/i.test(line)) continue;
        // Grab the first pipe-cell.
        const cells = line.split('|').map((c) => c.trim()).filter((c) => c.length > 0);
        if (cells.length === 0) continue;
        const first = cells[0];
        // Field name is backticked in this table; tolerate a stray row that
        // isn't and just skip it.
        const match = first.match(/^`([^`]+)`$/);
        if (!match) continue;
        fields.push(match[1]);
    }
    if (fields.length === 0) {
        return { fields: [], error: 'no documented fields found between markers' };
    }
    return { fields, error: null };
}

/**
 * Collect the union of all entry-level keys across every `mods[]` entry
 * in the parsed catalog.
 */
export function collectActualFields(catalog) {
    const all = new Set();
    for (const entry of catalog.mods ?? []) {
        for (const k of Object.keys(entry)) all.add(k);
    }
    return Array.from(all).sort();
}

/**
 * Given two string arrays, compute which are missing from each side.
 * `documented` is the README set; `actual` is what exists in catalog.json.
 */
export function diffFields({ documented, actual }) {
    const docSet = new Set(documented);
    const actSet = new Set(actual);
    return {
        missing_from_readme: actual.filter((f) => !docSet.has(f)).sort(),
        missing_from_catalog: documented.filter((f) => !actSet.has(f)).sort(),
    };
}

function main() {
    const readmeText = fs.readFileSync(README_PATH, 'utf8');
    const { fields: documented, error } = extractDocumentedFields(readmeText);
    if (error) {
        console.error(`[readme-schema] FAIL parsing README: ${error}`);
        process.exit(2);
    }

    let catalog;
    try {
        catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
    } catch (e) {
        console.error(`[readme-schema] FAIL parsing catalog.json: ${e.message}`);
        process.exit(2);
    }

    const actual = collectActualFields(catalog);
    const diff = diffFields({ documented, actual });

    console.log(`[readme-schema] documented=${documented.length} actual=${actual.length}`);

    if (diff.missing_from_readme.length === 0 && diff.missing_from_catalog.length === 0) {
        console.log('[readme-schema] OK — README table matches catalog.json 1:1.');
        process.exit(0);
    }

    console.error('[readme-schema] FAIL — README schema and catalog.json disagree:');
    if (diff.missing_from_readme.length) {
        console.error(`  Missing from README (present in catalog.json):`);
        for (const f of diff.missing_from_readme) console.error(`    - ${f}`);
    }
    if (diff.missing_from_catalog.length) {
        console.error(`  Missing from catalog.json (documented in README):`);
        for (const f of diff.missing_from_catalog) console.error(`    - ${f}`);
    }
    process.exit(1);
}

const invokedScriptName = path.basename(process.argv[1] ?? '');
if (invokedScriptName === 'check-readme-schema.mjs') {
    main();
}
