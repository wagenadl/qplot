# cmdrebalance.py - This file is part of QPlot

# QPlot - Publication quality 2D graphs with dual coordinate systems
# Copyright (C) 2014  Daniel Wagenaar
# (same GPL licence as original)

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from PyQt6.QtCore import QRectF

from .command import Command
from .token_ import Token
from .whichaxis import WhichAxis
from .range_ import Range
from .error import Error

if TYPE_CHECKING:
    from .statement import Statement
    from .figure import Figure
    from .panel import Panel
    from .axis import Axis


_SCALE_TOLERANCE = 2e-3
_SPACE_TOLERANCE = 1e-2  # pt


# ---------------------------------------------------------------------------
# SpaceNeeds — measurements for a group of panels along one axis
# ---------------------------------------------------------------------------

@dataclass
class SpaceNeeds:
    full_extent:       QRectF               = field(default_factory=QRectF)
    left_nondata_use:  dict[str, float]      = field(default_factory=dict)
    right_nondata_use: dict[str, float]      = field(default_factory=dict)
    data_range_map:    dict[str, Range]      = field(default_factory=dict)
    old_width:         dict[str, float]      = field(default_factory=dict)

    @staticmethod
    def build(f: Figure, ids: list[str],
              wa: WhichAxis) -> SpaceNeeds:
        sn = SpaceNeeds()

        # Get the union of desired extents across all panels in the group
        for id_ in ids:
            p = f.panel(id_)
            if sn.full_extent.isEmpty():
                sn.full_extent = p.desired_extent
            else:
                sn.full_extent = sn.full_extent.united(p.desired_extent)

        for id_ in ids:
            p = f.panel(id_)
            axis = wa.axis(p)
            desi_bb  = wa.rect_range(p.desired_extent)
            data_bb  = wa.axis_p_range(axis)
            sn.old_width[id_]         = desi_bb.range()
            sn.left_nondata_use[id_]  = data_bb.min() - desi_bb.min()
            sn.right_nondata_use[id_] = desi_bb.max() - data_bb.max()
            sn.data_range_map[id_]    = Range(axis.min(), axis.max())

        return sn

    def mean_old_width(self) -> float:
        if not self.old_width:
            return 0.0
        return sum(self.old_width.values()) / len(self.old_width)

    def max_left_nondata(self) -> float:
        return max(self.left_nondata_use.values(), default=0.0)

    def max_right_nondata(self) -> float:
        return max(self.right_nondata_use.values(), default=0.0)

    def max_nondata(self) -> float:
        return self.max_left_nondata() + self.max_right_nondata()

    def overall_data_range(self) -> Range:
        """Union of all panel data ranges in this group."""
        dr = Range()
        for r in self.data_range_map.values():
            dr.unionize(r)
        return dr


# ---------------------------------------------------------------------------
# Helper: parse ID blocks separated by dashes
# ---------------------------------------------------------------------------

def _blocks(s: Statement) -> list[list[str]]:
    """Parse 'ID ID ... - ID ID ... - ...' from token index 2 onward.
    Returns [] on any parse error or if any block has fewer than 2 IDs."""
    result: list[list[str]] = []
    current: list[str] = []

    for i in range(2, len(s)):
        if s[i].typ == Token.CAPITAL:
            current.append(s[i].str)
        elif s[i].typ == Token.DASH:
            if current:
                result.append(current)
            current = []
        else:
            return []  # unexpected token

    if current:
        result.append(current)

    if not result:
        return []
    if any(len(lst) < 2 for lst in result):
        return []

    return result


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def _rebalance(f: Figure, blks: list[list[str]],
               wa: WhichAxis) -> None:
    B = len(blks)
    if B == 0:
        return

    # Step 1: group each block by position along wa, check equal group count
    groups_by_block: list[list[list[str]]] = []
    needs_by_block:  list[list[SpaceNeeds]] = []
    N = -1  # groups per block

    for block in blks:
        groups = wa.ordered_groups(f, block)
        if N < 0:
            N = len(groups)
        if len(groups) != N:
            Error() << "Group mismatch"
            return
        groups_by_block.append(groups)
        needs_by_block.append(
            [SpaceNeeds.build(f, group, wa) for group in groups]
        )

    # Step 2: compute max non-data use per hypercolumn (column across blocks)
    hc_left_nondata:  list[float] = []
    hc_right_nondata: list[float] = []
    total_nondata = 0.0

    for n in range(N):
        lnd = max(needs[n].max_left_nondata()  for needs in needs_by_block)
        rnd = max(needs[n].max_right_nondata() for needs in needs_by_block)
        hc_left_nondata.append(lnd)
        hc_right_nondata.append(rnd)
        total_nondata += lnd + rnd

    # Step 3: full extent of each block
    full_extents: list[Range] = []
    for needs in needs_by_block:
        fe = Range()
        for need in needs:
            fe.unionize(wa.rect_range(need.full_extent))
        full_extents.append(fe)

    # Step 4: scale for first block, proposed widths per column
    scales: list[float] = []
    total_data = sum(
        need.overall_data_range().range()
        for need in needs_by_block[0]
    )
    scales.append((full_extents[0].range() - total_nondata) / total_data)

    trivial = True
    prop_width: list[float] = []
    for n in range(N):
        need = needs_by_block[0][n]
        desired = (hc_left_nondata[n] + hc_right_nondata[n]
                   + need.overall_data_range().range() * scales[0])
        prop_width.append(desired)
        if math.fabs(desired - need.mean_old_width()) > _SPACE_TOLERANCE:
            trivial = False

    # Step 5: scales for remaining blocks using same column widths
    for b in range(1, B):
        needs = needs_by_block[b]
        scl = -1.0
        for n in range(N):
            need = needs[n]
            dr   = need.overall_data_range().range()
            lnd  = hc_left_nondata[n]
            rnd  = hc_right_nondata[n]
            s    = (prop_width[n] - lnd - rnd) / dr
            if scl < 0 or s < scl:
                scl = s
            if math.fabs(prop_width[n] - need.mean_old_width()) > _SPACE_TOLERANCE:
                trivial = False
        scales.append(scl)

    triv_extent = trivial

    # Step 6: apply scale to all panels
    for b in range(B):
        needs = needs_by_block[b]
        x0    = full_extents[b].min()
        scale = scales[b]

        for n in range(N):
            need = needs[n]
            dr   = need.overall_data_range()
            x1   = x0 + prop_width[n]
            x_left = x0 + hc_left_nondata[n]

            for id_ in groups_by_block[b][n]:
                panel = f.panel_ref(id_)

                if not triv_extent:
                    ext = wa.rerect(panel.desired_extent, x0, x1)
                    f.override_panel_extent(id_, ext)

                axis = wa.axis(panel)
                rev  = wa.point(axis.maprel(1)) < 0
                x_right = x_left + dr.range() * scale
                px0 = x_right if rev else x_left
                px1 = x_left  if rev else x_right

                if (math.fabs(wa.point(axis.map(dr.min())) - px0)
                        > _SPACE_TOLERANCE):
                    trivial = False
                if (math.fabs(wa.point(axis.map(dr.max())) - px1)
                        > _SPACE_TOLERANCE):
                    trivial = False

                if not trivial:
                    axis.set_data_range(dr.min(), dr.max())
                    axis.set_placement(
                        wa.repoint(axis.minp(), px0),
                        wa.repoint(axis.maxp(), px1),
                    )

            x0 = x1

    if not trivial:
        f.mark_fudged()


# ---------------------------------------------------------------------------
# Command class
# ---------------------------------------------------------------------------

@Command.register("rebalance")
class CmdRebalance(Command):
    """Rearrange axis placements so panels share the same data scale.

    Syntax:
        rebalance x  ID [ID ...] [- ID [ID ...]] ...
        rebalance y  ID [ID ...] [- ID [ID ...]] ...
        rebalance xy ID [ID ...] [- ID [ID ...]] ...

    IDs within each dash-separated block are treated as a group.
    Note: does not work for rotated axes.
    """

    def _usage(self) -> bool:
        return self.error("Usage: rebalance x|y|xy ID ...\n")

    def parse(self, s: Statement) -> bool:
        if len(s) < 3:
            return self._usage()
        if s[1].typ != Token.BAREWORD:
            return self._usage()
        if s[1].str not in ("x", "y", "xy"):
            return self._usage()
        if not _blocks(s):
            return self._usage()
        return True

    def render(self, s: Statement, f: Figure, dryrun: bool) -> None:
        share_x = "x" in s[1].str
        share_y = "y" in s[1].str

        blks = _blocks(s)
        for blk in blks:
            for id_ in blk:
                if not f.has_panel(id_):
                    Error() << "Unknown panel: " << id_
                    return

        f.leave_panel()

        if share_x:
            _rebalance(f, blks, WhichAxis.x())
        if share_y:
            _rebalance(f, blks, WhichAxis.y())
