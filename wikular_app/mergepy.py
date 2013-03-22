#!/usr/bin/env python

import difflib

def diff3w(original, first_branch, second_branch):
    # strings with newlines
    had_conflict, merge = merge_files(
            first_branch.splitlines(1),
            original.splitlines(1),
            second_branch.splitlines(1))
    return ''.join(merge)

def drop_inline_diffs(diff):
    r = []
    for t in diff:
        if not t.startswith('?'):
            r.append(t)
    return r

def merge_files(a, x, b):
    dxa = difflib.Differ()
    dxb = difflib.Differ()
    xa = drop_inline_diffs(dxa.compare(x, a))
    xb = drop_inline_diffs(dxb.compare(x, b))

    m = []
    index_a = 0
    index_b = 0
    had_conflict = 0

    while (index_a < len(xa)) and (index_b < len(xb)):
        # no changes or adds on both sides
        if (xa[index_a] == xb[index_b] and
            (xa[index_a].startswith('  ') or xa[index_a].startswith('+ '))):
            m.append(xa[index_a][2:])
            index_a += 1
            index_b += 1
            continue

        # removing matching lines from one or both sides
        if ((xa[index_a][2:] == xb[index_b][2:])
            and (xa[index_a].startswith('- ') or xb[index_b].startswith('- '))):
            index_a += 1
            index_b += 1
            continue

        # adding lines in A
        if xa[index_a].startswith('+ ') and xb[index_b].startswith('  '):
            m.append(xa[index_a][2:])
            index_a += 1
            continue

        # adding line in B
        if xb[index_b].startswith('+ ') and xa[index_a].startswith('  '):
            m.append(xb[index_b][2:])
            index_b += 1
            continue

        # conflict - list both A and B, similar to GNU's diff3
        m.append("<<<<<<< A\n")
        while (index_a < len(xa)) and not xa[index_a].startswith('  '):
            m.append(xa[index_a][2:])
            index_a += 1
        m.append("=======\n")
        while (index_b < len(xb)) and not xb[index_b].startswith('  '):
            m.append(xb[index_b][2:])
            index_b += 1
        m.append(">>>>>>> B\n")
        had_conflict = 1

    # append remining lines - there will be only either A or B
    for i in range(len(xa) - index_a):
        m.append(xa[index_a + i][2:])
    for i in range(len(xb) - index_b):
        m.append(xb[index_b + i][2:])

    return had_conflict, m

