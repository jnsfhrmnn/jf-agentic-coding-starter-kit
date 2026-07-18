# QA Test Results Template

Add this section to the END of the feature spec `features/PROJ-X-feature-name.md`:

```markdown
---

## QA Test Results

**Tested:** YYYY-MM-DD
**Test Target:** [local app, CLI command, package, native build, preview URL, service endpoint, pipeline, generated artifact, document, or deployment target]
**Environment:** [OS/platform, runtime, device, hardware, relevant config]
**Tester:** QA / Verification Engineer (AI)
**Evidence:** commit:<sha> | file:<path>:<line> | test:<name> | url:<endpoint>

### Verification Commands
- [x] `[command or manual check]` - passed
- [ ] `[command or manual check]` - failed or not run; reason: [...]

### QA Scope Hardening
- **Required:** Yes / No
- **Reason:** [system/release/high-risk scope, or why not needed]
- **Scope Risks Found:** [missed journey/interface/data movement/platform/privacy/security/performance/AI-pipeline risk, or none]
- **Disposition:** [covered by tests/evidence, recorded as gap, routed to feature/spec/architecture, or N/A]

### Acceptance Criteria Status

#### AC-1: [Criterion Name]
- [x] Passed: [evidence]
- [ ] BUG: [describe failure]

#### AC-2: [Criterion Name]
- [x] Passed: [evidence]

### Master Goal / USP Alignment
- **Relevant Master Goal:** [section or criterion from docs/master-feature.md]
- **Contribution:** Strengthens / Neutral / Weakens / Unknown
- **Evidence:** [system behavior, test output, artifact, user journey result]
- **Gap:** [missing product-level capability, if any]

### System-Level Acceptance Criteria

#### MAC-1: [Master Criterion Name]
- [x] Passed: [evidence]
- [ ] Not tested: [reason]
- [ ] SYSTEM GAP: [gap blocking the whole product goal]

### Cross-Feature Journeys

#### Journey-1: [Journey Name]
- **Features / modules involved:** [PROJ-X, module, command, surface, process, service, artifact]
- [x] Passed: [evidence]
- [ ] BUG or GAP: [describe breakage or missing connection]

### Interfaces And Contracts
- [x] Surface to core boundary: [result or N/A]
- [x] Core to data/config/file boundary: [result or N/A]
- [x] Process/service/CLI/native/pipeline boundary: [result or N/A]
- [x] External integration or artifact contract: [result or N/A]
- [ ] BUG or GAP: [interface risk]

### Local / Cloud / Hybrid Verification
- **Expected Mode:** Offline/local | Online/cloud | Hybrid | Not applicable
- **Verified Data Movement:** [what stayed local, what left the trust boundary, what was logged/cached/retained]
- **Privacy/Security Controls:** [redaction, encryption, consent, access, retention, deletion, audit, or N/A]
- [x] Offline behavior verified: [result or N/A]
- [x] Remote/cloud behavior verified: [result or N/A]
- [ ] PRIVACY/MODE GAP: [mode mismatch or unverified boundary]

### Frontier AI / Pipeline Evaluation
- **Relevant Pipeline:** [AI/RAG/ML/media/GPU/evaluation/agentic/pipeline or N/A]
- **Quality Evidence:** [fixtures, benchmark, evaluation set, manual review, output comparison, or N/A]
- **Performance/Cost Evidence:** [latency, throughput, GPU/CPU/memory, cost estimate, or N/A]
- **Reproducibility Evidence:** [deterministic fixture, seed, model/version recorded, or N/A]
- [ ] GAP: [missing evidence or stale decision]

### Edge Cases Status

#### EC-1: [Edge Case Name]
- [x] Handled correctly

#### EC-2: [Edge Case Name]
- [ ] BUG: Expected [expected behavior], actual [actual behavior]

### Security / Safety / Robustness Review
- [x] Input validation: [result]
- [x] Authorization/ownership/data isolation: [result or N/A]
- [x] File/process/command handling: [result or N/A]
- [x] Secrets/sensitive output: [result]
- [x] External calls/cost/resource abuse: [result or N/A]
- [ ] BUG: [risk description]

### Regression / Verbund Review
- [x] Related approved/deployed features checked: [list]
- [x] Shared data, file, command, module, service, or artifact contracts checked: [result]
- [x] Critical product journeys still work: [result]
- [ ] BUG or GAP: [regression or untested critical dependency]

### Bugs Found

#### BUG-1: [Bug Title]
- **Severity:** Critical | High | Medium | Low
- **Environment:** [OS/runtime/config]
- **Steps to Reproduce:**
  1. Run/open [target]
  2. Perform [action/input]
  3. Expected: [what should happen]
  4. Actual: [what actually happens]
- **Evidence:** [log excerpt, screenshot, output file, failing assertion, artifact path]
- **Priority:** Fix before release | Fix in next iteration | Nice to have

### Summary
- **Acceptance Criteria:** X/Y passed
- **Master Acceptance Criteria:** X/Y passed, N not tested
- **Cross-Feature Journeys:** X/Y passed
- **Interfaces / Contracts:** Pass / Issues found / Not tested
- **Local / Cloud / Hybrid:** Verified / Issues found / Not tested / N/A
- **Frontier AI / Pipeline Evidence:** Pass / Issues found / Not tested / N/A
- **Bugs Found:** N total (C critical, H high, M medium, L low)
- **Security/Safety:** Pass / Issues found / Not applicable
- **Product Goal / USP:** Strengthened / Neutral / Weakened / Blocked
- **Missing Or Could-Be-Better:** [product-level gaps or feature candidates]
- **Release Ready:** YES / NO
- **Recommendation:** Release/package/deploy / Fix bugs first / Run system QA / Refine master feature / Re-run QA after changes
```
