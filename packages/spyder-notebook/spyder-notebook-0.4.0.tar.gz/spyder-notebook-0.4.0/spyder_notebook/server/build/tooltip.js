// Copyright (c) Jupyter Development Team, Spyder Project Contributors.
// Distributed under the terms of the Modified BSD License.
import { Text } from '@jupyterlab/coreutils';
import { Tooltip } from '@jupyterlab/tooltip';
import { Widget } from '@phosphor/widgets';
let tooltip = null;
export function dismissTooltip() {
    if (tooltip) {
        tooltip.dispose();
        tooltip = null;
    }
}
export function invokeTooltip(nbWidget) {
    const detail = 0;
    const parent = nbWidget.context;
    const anchor = nbWidget.content;
    const editor = anchor.activeCell.editor;
    const kernel = parent.session.kernel;
    const rendermime = anchor.rendermime;
    // If some components necessary for rendering don't exist, stop
    if (!editor || !kernel || !rendermime) {
        return;
    }
    if (tooltip) {
        tooltip.dispose();
        tooltip = null;
    }
    return fetchTooltip({ detail, editor, kernel })
        .then(bundle => {
        tooltip = new Tooltip({ anchor, bundle, editor, rendermime });
        Widget.attach(tooltip, document.body);
    })
        .catch(() => {
        /* Fails silently. */
    });
}
// A counter for outstanding requests.
let pending = 0;
/**
 * Fetch a tooltip's content from the API server.
 */
function fetchTooltip(options) {
    let { detail, editor, kernel } = options;
    let code = editor.model.value.text;
    let position = editor.getCursorPosition();
    let offset = Text.jsIndexToCharIndex(editor.getOffsetAt(position), code);
    // Clear hints if the new text value is empty or kernel is unavailable.
    if (!code || !kernel) {
        return Promise.reject(void 0);
    }
    let contents = {
        code,
        cursor_pos: offset,
        detail_level: detail || 0
    };
    let current = ++pending;
    return kernel.requestInspect(contents).then(msg => {
        let value = msg.content;
        // If a newer request is pending, bail.
        if (current !== pending) {
            return Promise.reject(void 0);
        }
        // If request fails or returns negative results, bail.
        if (value.status !== 'ok' || !value.found) {
            return Promise.reject(void 0);
        }
        return Promise.resolve(value.data);
    });
}
//# sourceMappingURL=tooltip.js.map