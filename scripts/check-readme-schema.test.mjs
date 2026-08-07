#!/usr/bin/env node
// Self-test for the README⇔catalog schema-parity gate.

import assert from 'node:assert/strict';
import {
    extractDocumentedFields,
    collectActualFields,
    diffFields,
} from './check-readme-schema.mjs';

function wrap(body) {
    return `prelude\n<!-- schema-table-begin -->\n${body}\n<!-- schema-table-end -->\ntrailer`;
}

function parses_a_well_formed_table() {
    const body = [
        '| Field | Type | Required | Scope | Notes |',
        '|---|---|---|---|---|',
        '| `id` | string | required | both | the id |',
        '| `kind` | enum | required | both | external or gpk |',
    ].join('\n');
    const { fields, error } = extractDocumentedFields(wrap(body));
    assert.equal(error, null);
    assert.deepEqual(fields, ['id', 'kind']);
}

function missing_markers_reports_error() {
    const { fields, error } = extractDocumentedFields('no markers here');
    assert.deepEqual(fields, []);
    assert.match(error, /markers/);
}

function empty_table_reports_error() {
    const body = '| Field | Type |\n|---|---|';
    const { error } = extractDocumentedFields(wrap(body));
    assert.match(error, /no documented fields/);
}

function tolerates_non_backticked_row() {
    const body = [
        '| Field | Type |',
        '|---|---|',
        '| `real_field` | string |',
        '| not_backticked | string |', // silently skipped
    ].join('\n');
    const { fields } = extractDocumentedFields(wrap(body));
    assert.deepEqual(fields, ['real_field']);
}

function collects_union_across_entries() {
    const catalog = {
        mods: [
            { id: 'a', kind: 'external', name: 'A', executable_relpath: 'x.exe' },
            { id: 'b', kind: 'gpk', name: 'B', target_patch: '100' },
        ],
    };
    const actual = collectActualFields(catalog);
    assert.deepEqual(actual, ['executable_relpath', 'id', 'kind', 'name', 'target_patch']);
}

function empty_catalog_yields_empty_actual_set() {
    const actual = collectActualFields({ mods: [] });
    assert.deepEqual(actual, []);
}

function diff_reports_both_directions() {
    const documented = ['id', 'name', 'documented_only'];
    const actual = ['id', 'name', 'catalog_only'];
    const d = diffFields({ documented, actual });
    assert.deepEqual(d.missing_from_readme, ['catalog_only']);
    assert.deepEqual(d.missing_from_catalog, ['documented_only']);
}

function diff_empty_when_sets_match() {
    const documented = ['id', 'name'];
    const actual = ['name', 'id']; // order shouldn't matter
    const d = diffFields({ documented, actual });
    assert.deepEqual(d.missing_from_readme, []);
    assert.deepEqual(d.missing_from_catalog, []);
}

function detector_flags_seeded_documentation_drift() {
    // Self-test: prove the gate actually bites if the two drift. A
    // silently-broken detector would rubber-stamp divergence.
    const readme = wrap(
        [
            '| Field | Type |',
            '|---|---|',
            '| `id` | string |',
            '| `only_documented` | string |',
        ].join('\n')
    );
    const catalog = {
        mods: [{ id: 'x', only_in_catalog: 'y' }],
    };
    const { fields: documented } = extractDocumentedFields(readme);
    const actual = collectActualFields(catalog);
    const d = diffFields({ documented, actual });
    assert.ok(
        d.missing_from_readme.includes('only_in_catalog'),
        'detector must flag catalog-only fields'
    );
    assert.ok(
        d.missing_from_catalog.includes('only_documented'),
        'detector must flag README-only fields'
    );
}

function run() {
    parses_a_well_formed_table();
    missing_markers_reports_error();
    empty_table_reports_error();
    tolerates_non_backticked_row();
    collects_union_across_entries();
    empty_catalog_yields_empty_actual_set();
    diff_reports_both_directions();
    diff_empty_when_sets_match();
    detector_flags_seeded_documentation_drift();
    console.log('check-readme-schema.test: ok (9 tests)');
}

run();
