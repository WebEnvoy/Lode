# LODE-231

## Static Facts

- Item ID: LODE-231
- Goal: 吸收 bb-sites 小红书/BOSS 站点知识并冻结 Lode 首批真实站点能力边界。
- Scope: 覆盖 Lode #230/#231/#232/#233/#234；只修改 Lode 文档和 LODE-231 事实载体。
- Execution Path: work/lode-231-bb-sites-knowledge
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-231.md
- Review Entry: .loom/reviews/LODE-231.json
- Validation Entry: python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check; loom fact-chain/verify/suite checks
- Closing Condition: PR 合并，#231-#234 与 #230 写入 closeout evidence 并关闭，随后 current pointer 回到 no_active_item。

## Covered Work Items

- #230 Absorb bb-sites site knowledge and freeze the first real capabilities.
- #231 Inventory absorbable bb-sites Xiaohongshu/BOSS material.
- #232 Map site entries, page types, and field sources.
- #233 Record source license, non-absorbable code, and trimming reasons.
- #234 Freeze first read and write-precheck capability boundaries.

## Associated Artifacts

- docs/contracts/bb-sites-xhs-boss-absorption-freeze.md
- docs/contracts/README.md
- README.md
- .loom/specs/LODE-231/**
