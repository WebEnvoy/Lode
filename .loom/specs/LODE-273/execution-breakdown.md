# Execution Breakdown

| Unit | Owner | Depends on | Evidence |
| --- | --- | --- | --- |
| Registry policy | Lode | #273 scope | local-packages validation |
| Operation policy | Lode | Registry policy | search/detail/validate-only self-tests |
| Schema enforcement | Lode | Operation policy | inversion negative tests |
| Review/merge | Main controller | All units | current-head reviews and hosted gate |
